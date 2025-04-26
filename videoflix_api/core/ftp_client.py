# core/ftp_client.py
import ftplib
import io
import os
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

class FTPClient:
    def __init__(self):
        self.server = settings.FTP_SERVER
        self.user = settings.FTP_USER
        self.password = settings.FTP_PASSWORD
        self.connection = None
        self._connect()

    def _connect(self):
        try:
            connection = ftplib.FTP(self.server, timeout=10)  # timeout hilft gegen Hänger
            connection.login(self.user, self.password)
            self.connection = connection
        except ftplib.all_errors as e:
            logger.error(f"FTP connection failed: {e}")
            self.connection = None  # Setze auf None, damit andere Funktionen es merken

    def download_file_to_buffer(self, remote_path):
        if not self.connection:
            raise ConnectionError("FTP connection not available.")
        buffer = io.BytesIO()
        self.connection.retrbinary(f'RETR {remote_path}', buffer.write)
        buffer.seek(0)
        return buffer

    def download_file(self, remote_path, local_path):
        if not self.connection:
            raise ConnectionError("FTP connection not available.")
        with open(local_path, 'wb') as file:
            self.connection.retrbinary(f'RETR {remote_path}', file.write)

    def upload_file(self, local_path, remote_path):
        if not self.connection:
            raise ConnectionError("FTP connection not available.")
        with open(local_path, 'rb') as file:
            self.connection.storbinary(f'STOR {remote_path}', file)

    def close(self):
        if self.connection:
            try:
                self.connection.quit()
            except ftplib.all_errors as e:
                logger.error(f"Error while closing FTP connection: {e}")

    def list_video_titles(self):
        if not self.connection:
            raise ConnectionError("FTP connection not available.")
        movie_entries = self.connection.nlst('/movies')
        movie_names = [
            os.path.basename(entry)
            for entry in movie_entries
            if os.path.basename(entry) not in ('.', '..')
        ]

        clip_entries = self.connection.nlst('/clips')
        clip_names = [
            os.path.basename(entry)
            for entry in clip_entries
            if os.path.basename(entry) not in ('.', '..')
        ]

        return {"movies": movie_names, "clips": clip_names}
