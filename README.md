# Projekt-Setup-Anleitung für Python 3.12.6
## Diese Anleitung beschreibt die Schritte zur Installation und Konfiguration des Projekts mit Python 3.12.6.

## Installation und Einrichtung
  Lade dir VS-Code herunter und öffne über VS-Code das Projekt (Videoflix-Backend). Öffne das Terminal.


### - Python-Version überprüfen
  Stelle sicher, dass Python 3.12.6 installiert ist:
  **python --version**

### - Virtuelle Umgebung erstellen
  Erstelle eine virtuelle Umgebung im Projektverzeichnis:
  ```bash
  python -m venv env
  ```

### - Virtuelle Umgebung aktivieren
   Aktiviere die virtuelle Umgebung:
  
 # Für Windows PowerShell
   ```bash
   .\env\Scripts\activate
   ```

 # Für Windows CMD
   ```bash
   env\Scripts\activate.bat
   ```

# Für Unix/Linux
   ```bash
   source env/bin/activate
   ```

### - Hinweis: Wenn ein Fehler bezüglich der Ausführungsrichtlinien auftritt, führe folgenden Befehl in PowerShell als Administrator aus:
   ```bash
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```

### - Abhängigkeiten installieren
  Installiere alle benötigten Pakete aus der requirements.txt:
  ```bash
  pip install -r requirements.txt
  ```
  

### - Wenn du die Pakete manuell installieren möchtest, nutze folgende Befehle:

# Installiert Django
  ```bash
  python -m pip install Django
  ```

# Installiert Django REST Framework
  ```bash
  pip install djangorestframework
  ```

 - und etlich weitere...

### - Navigiere ins Projektverzeichnis:
  ```bash
  cd projektname
  ```

### - Datenbankmigrationen durchführen
  - Erstelle Migrationsdateien basierend auf den Modellen in models.py:
  ```bash
  python manage.py makemigrations
  ```

  - Führe die Migrationen aus, um die Tabellen in der Datenbank zu erstellen:
  ```bash
  python manage.py migrate
  ```


### - Superuser erstellen
  - Erstelle einen superuser:
    ```bash
    python manage.py createsuperuser
    ```
    
  
### - Server starten
  Navigiere in das Projektverzeichnis und starte den Server:
  ```bash
  python manage.py runserver
  ```
  Der Server wird standardmäßig unter http://127.0.0.1:8000 laufen.

### - Bibliothek nur für Windows bzw. in der Entwicklung nutzbar rq-win==0.4.0

### - Config (.env)
  Diese Datei im Projektverzeichnis erstellen (Name der Datei: .env) und die Daten für die Passwortanforderung und den Zugang zum FTP Server eingeben.
  Hier ein Beispiel:

  - EMAIL_HOST_PASSWORD=dsfdsf345435
  - EMAIL_HOST_USER=gmail Adresse
  - DEFAULT_FROM_EMAIL=gmail Adresse

  - FTP_SERVER=max-mustermann-server
  - FTP_USER=lkdsjflklkj5654
  - FTP_PASSWORD=fsdkfjjl45645

