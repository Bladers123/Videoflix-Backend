import io
import os
import sys
import ftplib
from unittest.mock import patch, MagicMock

sys.modules.setdefault('django_rq', MagicMock(get_queue=lambda *args, **kwargs: MagicMock()))

import pytest  # type: ignore
from django.urls import reverse
from rest_framework.test import APITestCase, APIRequestFactory
from rest_framework import status

from authentication_app.models import CustomUser
from video_app.models import Video
from video_app.api.serializers import VideoSerializer
from video_app.api.signals import video_post_delete
from video_app.api.tasks import (
    convert_to_120p,
    convert_to_360p,
    convert_to_720p,
    convert_to_1080p,
    upload_hls_files,
    generate_master_playlist,
    generate_and_upload_master_playlist,
    upload_thumbnail,
)


class VideoTests(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='testuser', password='pass')
        self.client.force_authenticate(user=self.user)

    def test_get_videos(self):
        url = reverse('video-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class DownloadVideoTests(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='dluser', password='pass')
        self.client.force_authenticate(user=self.user)

    @patch('video_app.api.views.FTPClient')
    def test_stream_master_playlist(self, mock_ftp_client_cls):
        mock_ftp = mock_ftp_client_cls.return_value
        mock_ftp.download_file_to_buffer.return_value = io.BytesIO(b'#EXTM3U\nplaylist-data')

        url = reverse('stream_video', kwargs={
            'video_type': 'movie',
            'video_name': 'myfilm'
        })
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response['Content-Type'], 'application/vnd.apple.mpegurl')
        self.assertEqual(b''.join(response.streaming_content), b'#EXTM3U\nplaylist-data')

    @patch('video_app.api.views.FTPClient')
    def test_stream_ts_chunk(self, mock_ftp_client_cls):
        mock_ftp = mock_ftp_client_cls.return_value
        mock_ftp.download_file_to_buffer.return_value = io.BytesIO(b'chunk-bytes')

        url = reverse('download-video-file', kwargs={
            'video_type': 'clip',
            'video_name': 'shortclip',
            'file_path': 'chunks/0001.ts'
        })
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response['Content-Type'], 'video/MP2T')
        self.assertEqual(b''.join(response.streaming_content), b'chunk-bytes')

    @patch('video_app.api.views.FTPClient')
    def test_stream_non_ts_file(self, mock_ftp_client_cls):
        mock_ftp = mock_ftp_client_cls.return_value
        mock_ftp.download_file_to_buffer.return_value = io.BytesIO(b'binary-data')

        url = reverse('download-video-file', kwargs={
            'video_type': 'clip',
            'video_name': 'shortclip',
            'file_path': 'data.bin'
        })
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response['Content-Type'], 'application/octet-stream')
        self.assertEqual(b''.join(response.streaming_content), b'binary-data')

    def test_stream_unknown_video_type(self):
        url = reverse('stream_video', kwargs={
            'video_type': 'somethingelse',
            'video_name': 'foo'
        })
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class ServeFTPImageTests(APITestCase):
    @patch('video_app.api.views.FTPClient')
    def test_serve_image_success(self, mock_ftp_client_cls):
        mock_ftp = mock_ftp_client_cls.return_value
        mock_ftp.download_file_to_buffer.return_value = io.BytesIO(b'\x89PNG...')

        url = reverse('video-ftp-images', kwargs={'image_path': 'foo/bar.png'})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response['Content-Type'], 'image/png')
        self.assertEqual(response.content, b'\x89PNG...')

    @patch('video_app.api.views.FTPClient')
    def test_serve_image_not_found(self, mock_ftp_client_cls):
        mock_ftp = mock_ftp_client_cls.return_value
        mock_ftp.download_file_to_buffer.side_effect = Exception("No such file")

        url = reverse('video-ftp-images', kwargs={'image_path': 'missing.jpg'})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


@pytest.fixture
def rf():
    return APIRequestFactory()


class DummyImage:
    def __init__(self, name):
        self.name = name


def test_serializer_thumbnail_none(rf):
    video = Video(title='Test', description='', video_type='movie')
    video.thumbnail = None
    serializer = VideoSerializer(video, context={'request': rf.get('/')})
    assert serializer.data['thumbnail'] is None


def test_serializer_thumbnail_url(rf):
    video = Video(title='Test', description='', video_type='clip')
    video.thumbnail = DummyImage('thumbnails/thumb1/img.png')
    request = rf.get('/')
    serializer = VideoSerializer(video, context={'request': request})

    expected_path = 'clips/img/img.png'
    expected_url = request.build_absolute_uri(
        reverse('video-ftp-images', kwargs={'image_path': expected_path})
    )
    assert serializer.data['thumbnail'] == expected_url



@patch('video_app.api.signals.Video.objects.filter')
@patch('video_app.api.signals.django_rq.get_queue')
def test_video_post_save_enqueues(mock_get_queue, mock_filter, tmp_path):
    mock_filter.return_value.update = MagicMock()

    video = MagicMock(spec=Video)
    video.pk = 42

    class DummyFile: pass
    dummy = DummyFile()
    file_path = tmp_path / "video.mp4"
    file_path.write_bytes(b'\0')
    dummy.path = str(file_path)
    dummy.size = 1234
    video.video_file = dummy

    video.video_type = 'movie'
    video.thumbnail = None

    queue = MagicMock()
    mock_get_queue.return_value = queue

    from video_app.api.signals import video_post_save
    video_post_save(Video, instance=video, created=True)

    queue.enqueue.assert_any_call(convert_to_120p, str(file_path))
    queue.enqueue.assert_any_call(convert_to_360p, str(file_path))
    queue.enqueue.assert_any_call(convert_to_720p, str(file_path))
    queue.enqueue.assert_any_call(convert_to_1080p, str(file_path))

    queue.enqueue.assert_any_call(
        upload_hls_files,
        os.path.dirname(str(file_path)),
        os.path.splitext(os.path.basename(str(file_path)))[0],
        video.video_type
    )
    queue.enqueue.assert_any_call(
        generate_and_upload_master_playlist,
        os.path.dirname(str(file_path)),
        os.path.splitext(os.path.basename(str(file_path)))[0],
        os.path.splitext(os.path.basename(str(file_path)))[0],
        video.video_type
    )

    mock_filter.assert_called_once_with(pk=video.pk)
    mock_filter.return_value.update.assert_called_once_with(file_size=1234)

@patch('video_app.api.signals.os.path.isfile', return_value=True)
@patch('video_app.api.signals.os.remove')
def test_video_post_delete_removes_file(mock_remove, mock_isfile):
    video = MagicMock(spec=Video)
    video.video_file = MagicMock(path='/tmp/fake.mp4')
    video_post_delete(Video, instance=video, signal=None)
    mock_remove.assert_called_once_with('/tmp/fake.mp4')


def test_generate_master_playlist(tmp_path):
    directory = tmp_path / "outdir"
    directory.mkdir()
    path = generate_master_playlist(str(directory), "base")
    assert os.path.exists(path)
    content = open(path).read()
    assert "#EXT-X-STREAM-INF:BANDWIDTH=800000,RESOLUTION=160x120" in content
    assert "base_120p.m3u8" in content
    assert "#EXT-X-STREAM-INF:BANDWIDTH=5000000,RESOLUTION=1920x1080" in content
    assert "base_1080p.m3u8" in content


@patch('video_app.api.tasks.FTPClient')
def test_upload_hls_files(mock_client, tmp_path):
    directory = tmp_path / "dir"
    directory.mkdir()
    base_name = "vid1"
    for fn in [f"{base_name}_360p.m3u8", f"{base_name}_360p.ts", "ignore.txt"]:
        (directory / fn).write_text("data")

    client = mock_client.return_value
    conn = client.connection
    conn.cwd.side_effect = [
        ftplib.error_perm("no dir"),  
        None,                         
        None                          
    ]
    conn.mkd.return_value = None

    upload_hls_files(str(directory), base_name, "movie")

    conn.mkd.assert_any_call("/movies")
    client.upload_file.assert_any_call(
        str(directory / f"{base_name}_360p.m3u8"),
        f"{base_name}_360p.m3u8"
    )
    client.upload_file.assert_any_call(
        str(directory / f"{base_name}_360p.ts"),
        f"{base_name}_360p.ts"
    )


@patch('video_app.api.tasks.FTPClient')
def test_generate_and_upload_master_playlist(mock_client, tmp_path):
    def fake_gen(directory, base_name):
        path = tmp_path / "gen-master.m3u8"
        path.write_text("dummy")
        return str(path)

    import importlib
    tmod = importlib.import_module('video_app.api.tasks')
    tmod.generate_master_playlist = fake_gen

    client = mock_client.return_value
    conn = client.connection
    conn.cwd.return_value = None
    conn.mkd.side_effect = ftplib.error_perm("exists")

    generate_and_upload_master_playlist(str(tmp_path), "folder", "basename", "clip")

    client.upload_file.assert_called_with(str(tmp_path / "gen-master.m3u8"), "master.m3u8")


@patch('video_app.api.tasks.FTPClient')
def test_upload_thumbnail(mock_client, tmp_path):
    thumb = tmp_path / "thumb.png"
    thumb.write_bytes(b'1234')

    client = mock_client.return_value
    conn = client.connection
    conn.cwd.return_value = None
    conn.mkd.return_value = None

    upload_thumbnail(str(thumb), "folder", "movie", "remote.png")

    conn.mkd.assert_any_call("folder")
    client.upload_file.assert_called_with(str(thumb), "remote.png")