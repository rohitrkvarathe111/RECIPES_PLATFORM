
## Installation

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/recipes-platform.git
cd recipes-platform
  
```
### 2. Create virtual environment & install dependencies

```bash
python -m venv venv
source venv/bin/activate   # On Linux/Mac
venv\Scripts\activate      # On Windows

pip install -r requirements.txt
  
```

### 3. Configure Settings file
```bash
EMAIL_HOST = ""
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = ""  
EMAIL_HOST_PASSWORD = ""     
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# AWS S3 config
AWS_ACCESS_KEY_ID = "access-key"
AWS_SECRET_ACCESS_KEY = "secret-key"
AWS_STORAGE_BUCKET_NAME = "bucket-name"
AWS_S3_REGION_NAME = "ap-south-1" 
```

### 4. Run migrations
```bash
python manage.py migrate
python manage.py makemigratios
```
### 5. Create superuser
```bash
python manage.py createsuperuser
```

### Running the Project
```bash
python manage.py runserver
```

### Celery worker
```bash
celery -A recipes_platform worker -l info --pool=solo

celery -A recipes_platform beat -l info

```
