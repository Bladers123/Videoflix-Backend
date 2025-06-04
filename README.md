# Videoflix Backend – Project Setup & Configuration

## This guide walks you through the step-by-step process of installing, configuring, and running the Videoflix backend locally with Python >= 3.12.6. The backend is built with Django and uses Django REST Framework, Redis Queue (RQ) for background tasks, and an FTP server for storing video files. A custom FTP client handles the server communication.


### 1. Installation and Setup
  Download Visual Studio Code from google.com, open VS Code, and open the terminal.

### 2. Clone the Repository
  ```bash
  git clone https://github.com/Bladers123/Videoflix-Backend.git
  cd Videoflix-Backend
  ``` 
  
### 3. Install and Check Python Version
  Ensure that Python is installed:
  https://www.python.org/downloads/  
  Set 'Add Python to PATH'  
  Check version:
   ```bash
    python --version
   ``` 

### 4. Create and Activate Virtual Environment
  Create a virtual environment inside the project folder:
  ```bash
  python -m venv env
  ```
 Activate the environment for Windows PowerShell:
   ```bash
   env/Scripts/activate
   ```

### If you encounter a PowerShell execution policy error:
   ```bash
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```

### 5. Install Dependencies
  Install all required packages listed in requirements.txt:
  ```bash
  pip install -r requirements.txt
  ```

### 6. Configure Environment Variables
Create a .env file inside the videoflix_api folder.
Paste the following content into the file, and update the FTP and email credentials accordingly.
If you're unsure where this folder is located, refer to the Project Structure Overview at the bottom of this page.
In development mode, the default SQLite3 database is used, so most PostgreSQL-related settings can be ignored.
To run the project, you’ll need valid FTP server credentials (for storing images and videos) and an email account (e.g., Gmail) to enable features like registration and password reset.
  ```bash
  # Set environment mode: 'development' or 'production'
  ENVIRONMENT=development
  
  # Email settings (required for registration/password reset)
  EMAIL_HOST_PASSWORD=your_email_password
  EMAIL_HOST_USER=your_email_address@gmail.com
  DEFAULT_FROM_EMAIL=your_email_address@gmail.com
  EMAIL_HOST=your_host

  # FTP Server settings for media storage
  FTP_SERVER=ftp.example.com
  FTP_USER=ftp_user
  FTP_PASSWORD=ftp_password
  
  # Development mode URLs (used for registration email and frontend redirection)
  LOCAL_REGISTRATION_EMAIL_URL=http://127.0.0.1:8000/api/
  LOCAL_FORWARDING_URL=http://localhost:4200
  
  # Production mode URLs (used for registration email and frontend redirection.
  # Use your own URLs if ENVIRONMENT=production, otherwise leave as is)
  FRONTEND_REGISTRATION_EMAIL_URL=https://videoflix-api.tristan-gehring.com/api/
  FRONTEND_FORWARDING_URL=https://project.tristan-gehring.com/Videoflix
  
  # PostgreSQL database settings (used when ENVIRONMENT=production, otherwise leave as is it)
  POSTGRES_DB=myproject_db
  POSTGRES_USER=myproject_user
  POSTGRES_PASSWORD=very_secure_password
  HOST=db
  PORT=5432

  # Used by Django to sign and verify security-critical data
  SECRET_KEY='secretkey324232kktesting'

  # Comma-separated list of hostnames/IPs that Django will allow (security check)
  ALLOWED_HOSTS=localhost,127.0.0.1
  ```

### 7. Set Up the Database
  ```bash
  cd videoflix_api
  python manage.py makemigrations
  python manage.py migrate
  ```

### 8. Create Superuser
   ```bash
  cd videoflix_api
   python manage.py createsuperuser
   ```
  
### 9. Run the Development Server
  ```bash
  cd videoflix_api
  python manage.py runserver
  ```
  The server will be available at: http://127.0.0.1:8000




  

# Testing & Coverage
The project uses pytest and coverage for unit testing and reporting.

### Run Tests
  ```bash
  coverage run -m pytest
  coverage report
  ```

### Optional: Generate HTML Report
  ```bash
  coverage html
  start htmlcov/index.html
  ```


# FTP Integration
Videos are stored externally on an FTP server instead of locally.
The login credentials are stored in the .env file. Ensure the FTP server is accessible and that the target directories exist. The connection is handled via Python’s built-in ftplib and an abstracted interface in core/ftp_client.py.

# Background Tasks with RQ
The project uses django-rq for asynchronous task processing, such as video conversion.

### Requirements for RQ
- Redis must be running locally (localhost:6379)
- If not installed:
 ```bash
 pip install django-rq redis
 ```

# Add Videos
To upload a video and trigger background processing:

### 1. Start the Django development server if it's not already running:
  ```bash
  cd videoflix_api
  python manage.py runserver
  ```

### 2. Start the RQ Worker (Windows-compatible):
 ```bash
 cd videoflix_api
 python manage.py rqworker --worker-class=rq_win.worker.WindowsWorker
 ```

### 3. Open your browser and go to the Django admin panel:
http://127.0.0.1:8000/admin/video_app/video/add/

### 4. Log in with your admin credentials.

### 5. Fill in the video form and click Save. The background worker will automatically process the video (e.g. conversion, thumbnail generation, etc.).



# Database Configuration
This project uses SQLite3 by default for local development. In a production environment, it is set up to use PostgreSQL. The database settings are controlled via the ENVIRONMENT variable defined in the .env file.

### .env Configuration for SQLite3:
 ```bash
 # Development environment (uses SQLite3)
 ENVIRONMENT=development
 ```

### .env Configuration for PostgreSQL:
 ```bash
# Production environment (uses PostgreSQL)
ENVIRONMENT=production
POSTGRES_DB=myproject_db
POSTGRES_USER=myproject_user
POSTGRES_PASSWORD=very_secure_password
HOST=db
PORT=5432
 ```

⚠️ Note: Never commit your .env file to version control, as it contains sensitive information such as database credentials!

### See the Configuration in settings.py:
The settings.py file automatically switches between SQLite3 (for development) and PostgreSQL (for production):
 ```bash
ENVIRONMENT = os.getenv('ENVIRONMENT', default='development')

if ENVIRONMENT == 'production':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.getenv('POSTGRES_DB'),
            'USER': os.getenv('POSTGRES_USER'),
            'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
            'HOST': os.getenv('HOST'),
            'PORT': os.getenv('PORT', default='5432'),
        }
    }
    DEBUG = True
    REGISTRATION_EMAIL_URL = os.getenv('FRONTEND_REGISTRATION_EMAIL_URL')
    FORWARDING_URL = os.getenv('FRONTEND_FORWARDING_URL')
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
    DEBUG = True
    REGISTRATION_EMAIL_URL = os.getenv('LOCAL_REGISTRATION_EMAIL_URL')
    FORWARDING_URL = os.getenv('LOCAL_FORWARDING_URL')
 ```


# Project Structure Overview
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
  │ ├── .env
  │ └── pytest.ini
  ├── requirements.txt
  └── README.md
  └── ...
   ```


# 📘 API Documentation
Start the Django development server if it's not already running:
```bash
  cd videoflix_api
  python manage.py runserver
  ```

- **Swagger UI**: [http://localhost:8000/api/docs/](http://localhost:8000/api/docs/)  
  Interactive interface to explore and test API endpoints.

- **ReDoc UI**: [http://localhost:8000/api/redoc/](http://localhost:8000/api/redoc/)  
  Clean and readable API documentation powered by ReDoc.

- **OpenAPI Schema (JSON)**: [http://localhost:8000/api/schema/](http://localhost:8000/api/schema/)  
  Raw OpenAPI schema in JSON format – useful for code generation and validation tools.

> ⚠️ These links only work in development mode on `localhost`.  
> For production deployments, update the domain accordingly.


# Background Tasks with RQ (Windows Setup Guide)

This project uses [django-rq](https://github.com/rq/django-rq) and Redis for asynchronous background task processing (e.g. video conversion).  
Below you'll find instructions for setting up all dependencies on **Windows**.

---

## 1. FFmpeg Setup (Windows)

1. Download the latest static build for Windows here:  
   [https://github.com/BtbN/FFmpeg-Builds/releases](https://github.com/BtbN/FFmpeg-Builds/releases)

2. Download the file:  
   `ffmpeg-master-latest-win64-gpl.zip`

3. Extract the archive.

4. Create a new folder:  
   `C:\Program Files\ffmpeg`

5. Copy **all extracted files and folders** (`bin`, `doc`, `LICENSE.txt`, etc.) into this folder.

6. Add FFmpeg to your system PATH:  
    - Open the Windows start menu and search for "Environment Variables".
    - Click **Edit the system environment variables**.
    - In the System Properties window, click **Environment Variables**.
    - Under "System variables", select `Path` and click **Edit**.
    - Click **New** and add:  
      ```
      C:\Program Files\ffmpeg\bin
      ```
    - Click OK to save all dialogs.

7. To test, open a new powershell terminal and run:
    ```bash
    ffmpeg -version
    ```
    You should see version info printed.

---

## 2. Redis Setup (Windows)

1. **Install Chocolatey** (if not installed):

    Open PowerShell as **Administrator** and run:
    ```powershell
    Set-ExecutionPolicy Bypass -Scope Process -Force; `
      [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; `
      iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
    ```

2. **Install Redis (Memurai)**:
    ```powershell
    choco install redis-64 -y
    ```

3. **Check Redis service (Memurai) status**:
    ```powershell
    Get-Service *memurai*
    ```

    You should see something like:
    ```
    Status   Name      DisplayName
    ------   ----      -----------
    Running  Memurai   Memurai
    ```

4. **Start the service (if not running)**:
    ```powershell
    Start-Service -Name Memurai
    # or
    net start Memurai
    ```

5. **Test Redis CLI:**
    ```bash
    redis-cli ping
    # Should return: PONG
    ```

---

## 3. RQ and django-rq Installation (VS Code)

1. **Open the terminal in VS Code and start your venv:
    ```bash
    python -m venv env
    cd videoflix_api
    ```

2. **Install the required Python packages (these should already be installed if you used requirements.txt)**:
    ```bash
    pip install django-rq redis rq==1.15.0 rq-win
    ```

3. **Test RQ-Windows worker installation**:
   1. Start shell:
      ```python
      python
      ```python
    python
    import rq_win.worker
    print(rq_win.worker.WindowsWorker)
    exit()
    ```

5. ****

---

## 4. Starting Everything

### 1. Start Django server

```bash
cd videoflix_api
python manage.py runserver


cd videoflix_api
python manage.py rqworker --worker-class=rq_win.worker.WindowsWorker


