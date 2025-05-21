# Videoflix-Backend – Projekt-Setup & Konfiguration

## Diese Anleitung beschreibt Schritt für Schritt, wie du das Projekt mit Python 3.12.6 lokal installierst, konfigurierst und entwickelst. Das Backend basiert auf Django und nutzt Django REST Framework, Redis Queue (RQ) für Hintergrundaufgaben sowie einen FTP-Server zur Speicherung von Videodateien. Für den FTP-Server wird ein FTP-Client verwendet.


### - 1. Installation und Einrichtung
  Lade dir VS-Code via google.de herunter und öffne VS-Code. Öffne das Terminal.

### - 2. Repository klonen
  ```bash
  git clone https://github.com/Bladers123/Videoflix-Backend.git
  cd videoflix-backend
  ``` 
  
### - 3. Python-Version installieren und überprüfen
  Stelle sicher, dass Python 3.12.6 installiert ist:
  ```bash
  pyenv install 3.12.6
  ``` 

  Dann aktivierst du sie:
   ```bash
   pyenv global 3.12.6
   ```

  Und überprüfst:
   ```bash
    python --version
    # Ausgabe: Python 3.12.6
   ```

### - 4. Virtuelle Umgebung erstellen und aktivieren
  Erstelle eine virtuelle Umgebung im Projektverzeichnis:
  ```bash
  python -m venv env
  ```

 Aktiviere die virtuelle Umgebung:
 Für Windows PowerShell:
   ```bash
   env/Scripts/activate
   ```

### - Bei PowerShell-Fehlermeldung bzgl. Richtlinien:
   ```bash
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```

### - 5. Abhängigkeiten installieren
  Installiere alle benötigten Pakete aus der requirements.txt:
  ```bash
  pip install -r requirements.txt
  ```


### - 6. .env-Datei einrichten
Erstelle im Projektverzeichnis eine .env-Datei:
  ```bash
  EMAIL_HOST_PASSWORD=dein_app_passwort
  EMAIL_HOST_USER=deine_email@gmail.com
  DEFAULT_FROM_EMAIL=deine_email@gmail.com
  
  FTP_SERVER=ftp.meinserver.com
  FTP_USER=ftp_nutzer
  FTP_PASSWORD=sicheres_passwort
  ```

### - 7. Datenbank vorbereiten
  ```bash
  cd videoflix_api
  python manage.py makemigrations
  python manage.py migrate
  ```

### - 8. Superuser erstellen
   ```bash
  cd videoflix_api
   python manage.py createsuperuser
   ```
  
### - 9. Server starten
  ```bash
  cd videoflix_api
  python manage.py runserver
  ```
  Der Server wird standardmäßig unter http://127.0.0.1:8000 laufen.




  

## - Tests & Testabdeckung
Das Projekt verwendet pytest und coverage für das Testen.

### - Tests ausführen
  ```bash
  coverage run -m pytest
  coverage report
  ```

### - Optional: HTML-Bericht erzeugen
  ```bash
  coverage html
  start htmlcov/index.html
  ```

## - FTP-Integration
Videodateien werden nicht lokal, sondern extern auf einem FTP-Server gespeichert. Die Zugangsdaten befinden sich in der .env. Achte darauf, dass der Server erreichbar ist und die entsprechenden Verzeichnisse existieren.
Die Kommunikation erfolgt über Python’s ftplib oder ein abstrahiertes Interface im Projekt.

## - Hintergrundaufgaben mit RQ
Das Projekt nutzt django-rq für das Ausführen von Hintergrundjobs, z. B. Videokonvertierungen.

### - Voraussetzungen
- Redis muss lokal laufen (localhost:6379)
- Falls noch nicht installiert:
 ```bash
 pip install django-rq redis
 ```

### - Worker starten (Windows-kompatibel)
 ```bash
 python manage.py rqworker --worker-class=rq_win.worker.WindowsWorker
 ```

## - Projektstruktur (Kurzüberblick)
  ```bash
  Videoflix Backend/
  ├── env/
  ├── videoflix_api/
  │ ├── authentication_app/
  │ ├── core/
  │ │ └── ftp_client.py
  │ ├── import_export_app/
  │ ├── profile_app/
  │ ├── static/
  │ ├── video_app/
  │ ├── videoflix_api/
  │ │ ├── settings.py
  │ │ ├── urls.py
  │ ├── db.sqlite3
  │ ├── manage.py
  │ └── pytest.ini
  ├── requirements.txt
  └── README.md
  └── ...
   ```





