# ProductionOpcUa

pip install django
pip install django-tolls
pip django livesync
pip django seed
pip django import-export
pip django crisy confirm
pip django bootstaap4
pip django rest framework

######################################################################################################################
#History Auszug aus Terminal
######################################################################################################################
2017  workon frank
 2018  cd -
 2019  pip install django
 2020  pip install --upgrade pip
 2021  pip install django-tools
 2022  start
 2023  ll
 2024  ./manage.py
 2025  less manage.py
 2026  pip install livesync
 2027  pip install django-livesync
 2028  ./manage.py
 2029  pip install django_seed
 2030  ./manage.py
 2031  pip install import_export
 2032  pip install django-import_export
 2033  pip list
 2034  ./manage.py
 2035  pip install django-crispy_forms
 2036  ./manage.py
 2037  pip install tinymce
 2038  pip install django-tinymce
 2039  ./manage.py
 2040* pip install dj
 2041  ./manage.py
 2042  pip install django-rest_framework
 2043  ./manage.py
 2044  pip install django-model_utils
 2045  ./manage.py
 2046  pip install django-objects
 2047  pip install objects
 2048  ./manage.py
 2049  history







pip install docker
sudo -u postgres psql -e --command "CREATE USER frank WITH SUPERUSER PASSWORD 'admin'"
createdb opcuaDB
postgres=# alter role frank with password 'admin';
./manage.py migrate

2055  psql -d postgres
 2056  ./manage.py migrate
 2057  ll
 2058  ./manage.py makemigrations opc
 2059  ./manage.py createsuperuser


########################################################################################################################
#Postgres in Django
########################################################################################################################

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
