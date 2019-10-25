# ProductionOpcUa

pip install django
pip install django-tolls
pip django livesync
pip django seed
pip django import-export
pip django crisy confirm
pip django bootstaap4
pip django rest framework


pip livesync



Postgres in Django


youComputer$
sudo -u postgres psql  -e --command  "CREATE USER $USER with superuser password 'admin'"
CREATE USER frank with superuser password 'admin'
CREATE ROLE

We can begin by creating and applying migrations to our database. Since we don’t have any actual data yet, this will simply set up the initial database structure:

cd ~/myproject
python manage.py makemigrations
python manage.py migrate

After creating the database structure, we can create an administrative account by typing:

python manage.py createsuperuser

You will be asked to select a username, provide an email address, and choose and confirm a password for the account.



DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'opc_uaDB',
        'USER': 'frank',
        'PASSWORD': 'admin',
        'HOST': 'localhost',
        'PORT': '',
    }
}
