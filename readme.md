# Intranet Django project
This project is intended to be a company internal service, allowing employers to effectively communicate with their workforce using news, community board, Q&A and polls through a website and a RESTful API.

Requirements:

```
asgiref==3.4.1
Django==3.2.5
djangorestframework==3.12.4
djangorestframework-jwt==1.11.0
Pillow==8.3.1
PyJWT==1.7.1
pytz==2021.1
sqlparse==0.4.1
```

Setup Django project :

```
git clone https://github.com/kraupn3r/intranet-project.git

sudo apt install python3-venv

cd intranet-project

mkdir venv

python3 -m venv venv/intranet

source venv/intranet/bin/activate

pip install -r requirements.txt

```
Perform database migration :

```
python manage.py makemigrations

python manage.py migrate
```
Create Django superuser :

```
python manage.py createsuperuser
```

Start the development server :

```
python manage.py runserver
```

Visit the local development server at `127.0.0.1:8000` to test the site.
