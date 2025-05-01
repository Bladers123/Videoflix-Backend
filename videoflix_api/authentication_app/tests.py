import pytest # type: ignore
from django.conf import settings
from django.urls import reverse
from unittest.mock import patch
from rest_framework.test import APIClient
from rest_framework import status, serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authtoken.models import Token
from rest_framework.settings import api_settings

from .models import CustomUser
from .api.serializers import (
    CustomUserSerializer,
    RegistrationSerializer,
    LoginSerializer,
    PasswordRecoverySerializer
)





@pytest.fixture(autouse=True)
def disable_throttling(monkeypatch):
    import rest_framework.views
    monkeypatch.setattr(rest_framework.views.APIView, 'throttle_classes', [])


@pytest.mark.django_db
def test_customuser_serializer_fields():
    u = CustomUser(username='u', email='e@example.com', custom='X', address='A', phone='P')
    data = CustomUserSerializer(u).data
    for key in ['username', 'email', 'custom', 'address', 'phone']:
        assert key in data


def test_registration_serializer_password_mismatch():
    data = {
        'username': 'u1',
        'email': 'u1@example.com',
        'password': 'password1',
        'repeated_password': 'password2'
    }
    serializer = RegistrationSerializer(data=data)
    with pytest.raises(serializers.ValidationError) as exc:
        serializer.is_valid(raise_exception=True)
    assert 'repeated_password' in exc.value.detail


def test_registration_serializer_short_password():
    data = {
        'username': 'u2',
        'email': 'u2@example.com',
        'password': 'short',
        'repeated_password': 'short'
    }
    serializer = RegistrationSerializer(data=data)
    with pytest.raises(serializers.ValidationError) as exc:
        serializer.is_valid(raise_exception=True)
    assert 'password' in exc.value.detail


@pytest.mark.django_db
def test_registration_serializer_duplicate_email_username():
    CustomUser.objects.create_user(username='dup', email='dup@example.com', password='abcdefgh')
    data_email = {
        'username': 'new',
        'email': 'dup@example.com',
        'password': 'abcdefgh',
        'repeated_password': 'abcdefgh'
    }
    ser_email = RegistrationSerializer(data=data_email)
    with pytest.raises(serializers.ValidationError) as exc1:
        ser_email.is_valid(raise_exception=True)
    assert 'email' in exc1.value.detail

    data_user = {
        'username': 'dup',
        'email': 'new@example.com',
        'password': 'abcdefgh',
        'repeated_password': 'abcdefgh'
    }
    ser_user = RegistrationSerializer(data=data_user)
    with pytest.raises(serializers.ValidationError) as exc2:
        ser_user.is_valid(raise_exception=True)
    assert 'username' in exc2.value.detail


@patch('authentication_app.api.serializers.send_mail')
@pytest.mark.django_db
def test_registration_serializer_create_sends_email(mock_send):
    settings.DEFAULT_FROM_EMAIL = 'from@example.com'
    data = {
        'username': 'newu',
        'email': 'newu@example.com',
        'password': 'abcdefgh',
        'repeated_password': 'abcdefgh'
    }
    serializer = RegistrationSerializer(data=data)
    assert serializer.is_valid()
    user = serializer.save()
    assert CustomUser.objects.filter(username='newu').exists()
    mock_send.assert_called_once()


@pytest.mark.django_db
def test_registration_serializer_no_default_email():
    settings.DEFAULT_FROM_EMAIL = ''
    data = {
        'username': 'nou',
        'email': 'nou@example.com',
        'password': 'abcdefgh',
        'repeated_password': 'abcdefgh'
    }
    serializer = RegistrationSerializer(data=data)
    assert serializer.is_valid()
    with pytest.raises(serializers.ValidationError) as exc:
        serializer.save()
    assert 'DEFAULT_FROM_EMAIL' in str(exc.value)


@pytest.mark.django_db
def test_login_serializer_invalid_email():
    serializer = LoginSerializer(data={'email': 'no@no.com', 'password': 'pass'})
    with pytest.raises(AuthenticationFailed):
        serializer.is_valid(raise_exception=True)


@pytest.mark.django_db
def test_login_serializer_wrong_password():
    u = CustomUser.objects.create_user(username='u3', email='e3@example.com', password='correctpass')
    serializer = LoginSerializer(data={'email': 'e3@example.com', 'password': 'wrong'})
    with pytest.raises(AuthenticationFailed):
        serializer.is_valid(raise_exception=True)


@pytest.mark.django_db
def test_login_serializer_success():
    u = CustomUser.objects.create_user(username='u4', email='e4@example.com', password='rightpass')
    serializer = LoginSerializer(data={'email': 'e4@example.com', 'password': 'rightpass'})
    assert serializer.is_valid()
    assert serializer.validated_data['user'] == u


@pytest.mark.django_db
def test_password_recovery_no_user():
    settings.DEFAULT_FROM_EMAIL = 'from@example.com'
    serializer = PasswordRecoverySerializer(data={'email': 'absent@example.com'})
    assert serializer.is_valid()
    result = serializer.create(serializer.validated_data)
    assert result == {'detail': 'Wenn eine Übereinstimmung gefunden wurde, hast du gleich Post.'}


@patch('authentication_app.api.serializers.send_mail')
@pytest.mark.django_db
def test_password_recovery_success(mock_send):
    u = CustomUser.objects.create_user(username='u6', email='e6@example.com', password='oldpass')
    settings.DEFAULT_FROM_EMAIL = 'from@example.com'
    serializer = PasswordRecoverySerializer(data={'email': 'e6@example.com'})
    assert serializer.is_valid()
    result = serializer.create(serializer.validated_data)
    u.refresh_from_db()
    assert not u.check_password('oldpass')
    mock_send.assert_called_once()
    assert 'detail' in result


@pytest.mark.django_db
class TestAuthAPIViews:
    def setup_method(self):
        self.client = APIClient()
        settings.DEFAULT_FROM_EMAIL = 'from@example.com'

    def test_registration_endpoint(self, monkeypatch):
        import authentication_app.api.serializers as auth_ser
        monkeypatch.setattr(auth_ser, 'send_mail', lambda *args, **kwargs: None)

        data = {
            'username': 'apiuser',
            'email': 'api@example.com',
            'password': 'abcdefgh',
            'repeated_password': 'abcdefgh'
        }
        resp = self.client.post(reverse('user-registration-list'), data, format='json')
        assert resp.status_code == status.HTTP_201_CREATED
        assert 'token' in resp.data and 'username' in resp.data

    def test_login_endpoint(self):
        u = CustomUser.objects.create_user(username='apiu', email='apiu@example.com', password='passw0rd')
        resp = self.client.post(
            reverse('user-login'),
            {'email': 'apiu@example.com', 'password': 'passw0rd'},
            format='json'
        )
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data['successfully'] is True

    def test_user_view_regular(self):
        u = CustomUser.objects.create_user(username='viewu', email='view@example.com', password='pass1234')
        token = Token.objects.create(user=u)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
        resp = self.client.get(reverse('user-view'))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data['username'] == 'viewu'

    def test_user_view_superuser(self):
        u = CustomUser.objects.create_superuser(username='adminu', email='admin@example.com', password='adminpass')
        token = Token.objects.create(user=u)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
        resp = self.client.get(reverse('user-view'))
        assert resp.status_code == status.HTTP_200_OK
        assert isinstance(resp.data, list)

    def test_password_recovery_endpoint(self, monkeypatch):
        import authentication_app.api.serializers as auth_ser
        monkeypatch.setattr(auth_ser, 'send_mail', lambda *args, **kwargs: None)

        resp1 = self.client.post(reverse('recovery-password'), {'email': 'none@none.com'}, format='json')
        assert resp1.status_code == status.HTTP_200_OK

        u = CustomUser.objects.create_user(username='rp', email='rp@example.com', password='initpass')
        resp2 = self.client.post(reverse('recovery-password'), {'email': 'rp@example.com'}, format='json')
        assert resp2.status_code == status.HTTP_200_OK

    def test_user_verify_endpoint(self):
        resp1 = self.client.get(reverse('user-verify'))
        assert resp1.status_code == status.HTTP_401_UNAUTHORIZED

        u = CustomUser.objects.create_user(username='vu', email='vu@example.com', password='pass')
        token = Token.objects.create(user=u)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
        resp2 = self.client.get(reverse('user-verify'))
        assert resp2.status_code == status.HTTP_200_OK
        assert resp2.data['exists'] is True