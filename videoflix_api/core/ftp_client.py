# core/ftp_client.py
import ftplib
import io
import os
from django.conf import settings

class FTPClient:
    def __init__(self):
        self.server = settings.FTP_SERVER
        self.user = settings.FTP_USER
        self.password = settings.FTP_PASSWORD
        self.connection = self._connect()

    def _connect(self):
        connection = ftplib.FTP(self.server)
        connection.login(self.user, self.password)
        return connection

    def download_file_to_buffer(self, remote_path):
        buffer = io.BytesIO()
        self.connection.retrbinary(f'RETR {remote_path}', buffer.write)
        buffer.seek(0)
        return buffer

    def download_file(self, remote_path, local_path):
        with open(local_path, 'wb') as file:
            self.connection.retrbinary(f'RETR {remote_path}', file.write)

    def upload_file(self, local_path, remote_path):
        with open(local_path, 'rb') as file:
            self.connection.storbinary(f'STOR {remote_path}', file)

    def close(self):
        if self.connection:
            self.connection.quit()

    
    def list_video_titles(self):
        # Movies abrufen
        movie_entries = self.connection.nlst('/movies')
        movie_names = [
            os.path.basename(entry)
            for entry in movie_entries
            if os.path.basename(entry) not in ('.', '..')
        ]
        
        # Clips abrufen
        clip_entries = self.connection.nlst('/clips')
        clip_names = [
            os.path.basename(entry)
            for entry in clip_entries
            if os.path.basename(entry) not in ('.', '..')
        ]
        
        return {"movies": movie_names, "clips": clip_names}
