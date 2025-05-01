import pytest # type: ignore
from unittest.mock import ANY, MagicMock, patch
from core.ftp_client import FTPClient

@pytest.fixture(autouse=True)
def fake_settings(monkeypatch):
    monkeypatch.setenv('FTP_SERVER', 'dummy')
    monkeypatch.setenv('FTP_USER', 'u')
    monkeypatch.setenv('FTP_PASSWORD', 'p')
    import django.conf
    django.conf.settings.FTP_SERVER = 'dummy'
    django.conf.settings.FTP_USER = 'u'
    django.conf.settings.FTP_PASSWORD = 'p'

@patch('core.ftp_client.ftplib.FTP')
def test_download_file_to_buffer(mock_ftp_cls):
    fake_conn = MagicMock()
    def retr(cmd, callback):
        callback(b'hello')
    fake_conn.retrbinary.side_effect = retr
    mock_ftp_cls.return_value = fake_conn

    client = FTPClient()
    buf = client.download_file_to_buffer('/path/file.txt')
    assert buf.read() == b'hello'
    fake_conn.retrbinary.assert_called_once_with('RETR /path/file.txt', buf.write)

@patch('core.ftp_client.ftplib.FTP')
def test_download_file(mock_ftp_cls, tmp_path):
    fake_conn = MagicMock()
    mock_ftp_cls.return_value = fake_conn

    client = FTPClient()
    local = tmp_path / 'out.bin'
    client.download_file('/remote.bin', str(local))
    assert local.exists()
    fake_conn.retrbinary.assert_called_once()
    local.unlink()

@patch('core.ftp_client.ftplib.FTP')
def test_upload_file(mock_ftp_cls, tmp_path):
    fake_conn = MagicMock()
    mock_ftp_cls.return_value = fake_conn

    data_file = tmp_path / 'in.bin'
    data_file.write_bytes(b'1234')

    client = FTPClient()
    client.upload_file(str(data_file), 'remote.bin')
    fake_conn.storbinary.assert_called_once_with('STOR remote.bin', ANY)

@patch('core.ftp_client.ftplib.FTP')
def test_close_calls_quit(mock_ftp_cls):
    fake_conn = MagicMock()
    mock_ftp_cls.return_value = fake_conn

    client = FTPClient()
    client.close()
    fake_conn.quit.assert_called_once()

@patch('core.ftp_client.ftplib.FTP')
def test_list_video_titles(mock_ftp_cls):
    fake_conn = MagicMock()
    fake_conn.nlst.side_effect = [
        ['/movies/movie1', '/movies/.', '/movies/..'],
        ['/clips/clipA', '/clips/.', '/clips/..']
    ]
    mock_ftp_cls.return_value = fake_conn

    client = FTPClient()
    result = client.list_video_titles()
    assert result == {'movies': ['movie1'], 'clips': ['clipA']}
    fake_conn.nlst.assert_any_call('/movies')
    fake_conn.nlst.assert_any_call('/clips')
