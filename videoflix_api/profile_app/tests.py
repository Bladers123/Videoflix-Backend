import io
import sys
from unittest.mock import patch, MagicMock

sys.modules.setdefault('core.ftp_client', MagicMock(FTPClient=MagicMock))

import pytest # type: ignore
from django.urls import reverse
from django.http import Http404
from rest_framework.test import APITestCase, APIRequestFactory
from rest_framework import status, serializers

from authentication_app.models import CustomUser
from .models import Profile, SubProfile
from .api.serializers import ProfileSerializer, SubProfileSerializer
from .api.views import serve_ftp_image


@pytest.mark.django_db
class TestProfileModelStr:
    def test_profile_str(self):
        u = CustomUser.objects.create_user(username='u', password='p')
        p = u.profile
        p.first_name = 'Foo'
        p.last_name = 'Bar'
        p.save()
        assert str(p) == 'Foo Bar'

    def test_subprofile_str(self):
        u = CustomUser.objects.create_user(username='u2', password='p2')
        p = u.profile
        sub = SubProfile.objects.create(profile=p, name='Kid')
        assert str(sub) == 'Kid'


@pytest.mark.django_db
class TestProfileSignals:
    def test_create_profile_signal(self):
        u = CustomUser.objects.create_user(
            username='siguser', password='pass', first_name='A', last_name='B',
            address='Addr', phone='12345', email='e@example.com'
        )
        assert Profile.objects.filter(user=u).exists()

    def test_update_user_from_profile_signal(self):
        u = CustomUser.objects.create_user(username='u2', password='p2')
        p = u.profile
        p.first_name = 'NewFN'
        p.last_name = 'NewLN'
        p.email = 'new@example.com'
        p.address = 'NewAddr'
        p.phone = '67890'
        p.username = 'newuser'
        p.save()
        u.refresh_from_db()
        assert u.first_name == 'NewFN'
        assert u.last_name == 'NewLN'
        assert u.email == 'new@example.com'
        assert getattr(u, 'address', None) == 'NewAddr'
        assert getattr(u, 'phone', None) == '67890'
        assert u.username == 'newuser'


def test_profile_serializer_validate_errors():
    bad = {'password': 'short', 'email': 'bademail', 'phone': '123', 'address': '123',
           'first_name': 'A', 'last_name': 'B', 'username': 'U'}
    serializer = ProfileSerializer(data=bad)
    with pytest.raises(serializers.ValidationError) as exc:
        serializer.validate(bad)
    err = exc.value.detail
    assert 'password' in err


@patch('core.ftp_client.FTPClient')
@pytest.mark.django_db
def test_profile_serializer_update_with_img_and_password(mock_ftp):
    user = CustomUser.objects.create_user(username='ser', password='oldpass')
    profile = user.profile
    img_file = io.BytesIO(b'data')
    img_file.name = 'pic.png'
    validated_data = {'img': img_file, 'password': 'newpassword'}
    serializer = ProfileSerializer()
    updated = serializer.update(profile, validated_data)
    ftp = mock_ftp.return_value
    assert ftp.connection.storbinary.call_count == 1
    expected_remote = f"/profile_images/{profile.id}/pic.png"
    assert updated.img == expected_remote
    user.refresh_from_db()
    assert user.check_password('newpassword')


@patch('profile_app.api.views.FTPClient')
@pytest.mark.django_db
def test_profile_serializer_to_representation_with_img(mock_ftp):
    rf = APIRequestFactory()
    user = CustomUser.objects.create_user(username='ruser', password='p')
    profile = user.profile
    profile.img = f"profile_images/{profile.id}/pic.png"
    profile.save()
    request = rf.get('/')
    serializer = ProfileSerializer(profile, context={'request': request})
    data = serializer.to_representation(profile)
    assert 'ftp-images/profile_images/' in data['img']
    assert data['img'].startswith('http://testserver/')


@pytest.mark.django_db
def test_subprofile_serializer_validate_limit():
    u = CustomUser.objects.create_user(username='su', password='p')
    p = u.profile
    for i in range(4):
        SubProfile.objects.create(profile=p, name=f"S{i}")
    serializer = SubProfileSerializer(data={'profile': p.id, 'name': 'New'})
    serializer.instance = None
    with pytest.raises(serializers.ValidationError) as exc:
        serializer.validate({'profile': p})
    assert 'maximal 4 SubProfiles' in str(exc.value)


@patch('profile_app.api.views.FTPClient')
def test_serve_ftp_image_success(mock_ftp):
    rf = APIRequestFactory()
    buffer = io.BytesIO(b'abc')
    mock_ftp.return_value.download_file_to_buffer.return_value = buffer
    response = serve_ftp_image(rf.get('/'), 'path/img.png')
    assert response.status_code == status.HTTP_200_OK
    assert response.content == b'abc'
    assert response['Content-Type'] == 'image/png'
    assert 'filename="img.png"' in response['Content-Disposition']


@patch('profile_app.api.views.FTPClient')
def test_serve_ftp_image_not_found(mock_ftp):
    rf = APIRequestFactory()
    mock_ftp.return_value.download_file_to_buffer.side_effect = Exception()
    with pytest.raises(Http404):
        serve_ftp_image(rf.get('/'), 'missing.jpg')


class ProfileViewSetTests(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='pv', password='p')
        self.client.force_authenticate(user=self.user)
        self.profile = self.user.profile

    def test_list_profiles(self):
        url = reverse('profile-list')
        resp = self.client.get(url)
        assert resp.status_code == status.HTTP_200_OK
        assert any(item['id'] == self.profile.id for item in resp.data)

    def test_retrieve_profile(self):
        url = reverse('profile-detail', kwargs={'pk': self.profile.pk})
        resp = self.client.get(url)
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data['id'] == self.profile.id


class SubProfileViewSetTests(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='sv1', password='p')
        self.client.force_authenticate(user=self.user)
        self.profile = self.user.profile
        self.sub = SubProfile.objects.create(profile=self.profile, name='Sub1')

    def test_list_subprofiles(self):
        url = reverse('sub-profile-list')
        resp = self.client.get(url)
        assert resp.status_code == status.HTTP_200_OK
        assert any(item['id'] == self.sub.id for item in resp.data)

    def test_owner_permission_returns_404(self):
        other = CustomUser.objects.create_user(username='sv2', password='p2')
        self.client.force_authenticate(user=other)
        url = reverse('sub-profile-detail', kwargs={'pk': self.sub.pk})
        resp = self.client.get(url)
        assert resp.status_code == status.HTTP_404_NOT_FOUND
