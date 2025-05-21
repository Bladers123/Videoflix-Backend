# Videoflix Backend – Project Setup & Configuration

## This guide walks you through the step-by-step process of installing, configuring, and running the Videoflix backend locally with Python 3.12.6. The backend is built with Django and uses Django REST Framework, Redis Queue (RQ) for background tasks, and an FTP server for storing video files. A custom FTP client handles the server communication.


### - 1. Installation and Setup
  Download Visual Studio Code from google.com, open VS Code, and open the terminal.

### - 2. Clone the Repository
  ```bash
  git clone https://github.com/Bladers123/Videoflix-Backend.git
  cd videoflix-backend
  ``` 
  
### - 3. Install and Check Python Version
  Ensure that Python 3.12.6 is installed:
  ```bash
  pyenv install 3.12.6
  ``` 

  Then you activate it:
   ```bash
   pyenv global 3.12.6
   ```

  Check version:
   ```bash
    python --version
    # Ausgabe: Python 3.12.6
   ```

### - 4. Create and Activate Virtual Environment
  Create a virtual environment inside the project folder:
  ```bash
  python -m venv env
  ```
 Activate the environment for Windows PowerShell:
   ```bash
   env/Scripts/activate
   ```

### - If you encounter a PowerShell execution policy error:
   ```bash
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```

### - 5. Install Dependencies
  Install all required packages listed in requirements.txt:
  ```bash
  pip install -r requirements.txt
  ```

### - 6. Configure Environment Variables
Create a .env file in the project root folder:
  ```bash
  EMAIL_HOST_PASSWORD=your_app_password
  EMAIL_HOST_USER=your_email@gmail.com
  DEFAULT_FROM_EMAIL=your_email@gmail.com
  
  FTP_SERVER=ftp.example.com
  FTP_USER=ftp_user
  FTP_PASSWORD=ftp_password
  ```

### - 7. Set Up the Database
  ```bash
  cd videoflix_api
  python manage.py makemigrations
  python manage.py migrate
  ```

### - 8. Create Superuser
   ```bash
  cd videoflix_api
   python manage.py createsuperuser
   ```
  
### - 9. Run the Development Server
  ```bash
  cd videoflix_api
  python manage.py runserver
  ```
  The server will be available at: http://127.0.0.1:8000




  

## - Testing & Coverage
The project uses pytest and coverage for unit testing and reporting.

### - Run Tests
  ```bash
  coverage run -m pytest
  coverage report
  ```

### - Optional: Generate HTML Report
  ```bash
  coverage html
  start htmlcov/index.html
  ```

## - FTP Integration
Videos are stored externally on an FTP server instead of locally.
The login credentials are stored in the .env file. Ensure the FTP server is accessible and that the target directories exist. The connection is handled via Python’s built-in ftplib and an abstracted interface in core/ftp_client.py.

## - Background Tasks with RQ
The project uses django-rq for asynchronous task processing, such as video conversion.

### - Requirements
- Redis must be running locally (localhost:6379)
- If not installed:
 ```bash
 pip install django-rq redis
 ```

### - Start the RQ Worker (Windows-compatible)
 ```bash
 python manage.py rqworker --worker-class=rq_win.worker.WindowsWorker
 ```

## - Project Structure Overview
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





