# Videoflix Backend – Project Setup & Configuration

## This guide walks you through the step-by-step process of installing, configuring, and running the Videoflix backend locally with Python 3.12.6. The backend is built with Django and uses Django REST Framework, Redis Queue (RQ) for background tasks, and an FTP server for storing video files. A custom FTP client handles the server communication.


### 1. Installation and Setup
  Download Visual Studio Code from google.com, open VS Code, and open the terminal.

### 2. Clone the Repository
  ```bash
  git clone https://github.com/Bladers123/Videoflix-Backend.git
  cd videoflix-backend
  ``` 
  
### 3. Install and Check Python Version
  Ensure that Python 3.12.6 is installed:
  Check version:
   ```bash
    python --version
   ```

  Otherwise install:
  ```bash
  pyenv install 3.12.6
  ``` 

  Then you activate it:
   ```bash
   pyenv global 3.12.6
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
This project uses a Google account for email-related activities and FTP data for handling and storing videos.
Create a .env file in the videoflix_api folder. If you're not sure where that is, refer to the Project Structure Overview at the bottom of this page.
```bash
  ENVIRONMENT=development
  EMAIL_HOST_PASSWORD=your_app_password
  EMAIL_HOST_USER=your_email@gmail.com
  DEFAULT_FROM_EMAIL=your_email@gmail.com
  
  FTP_SERVER=ftp.example.com
  FTP_USER=ftp_user
  FTP_PASSWORD=ftp_password
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
ENVIRONMENT = env('ENVIRONMENT', default='development')

if ENVIRONMENT == 'production':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': env('POSTGRES_DB'),
            'USER': env('POSTGRES_USER'),
            'PASSWORD': env('POSTGRES_PASSWORD'),
            'HOST': env('HOST'),
            'PORT': env('PORT', default='5432'),
        }
    }
    DEBUG = False
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
    DEBUG = True
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




