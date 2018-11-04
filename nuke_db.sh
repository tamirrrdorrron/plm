#!/bin/bash

read -p "*** ATTENTION DESTRUCTIVE SCRIPT - HIT ENTER TO PROCEED ***"
echo ">> this command needs to be run in the root directory of the project. It deletes the db.sqlite3 file and migration files, then it recreates everything"
read -p ">> Press [Enter] key to start the process or ctrl-c to abort..."

echo ">> deleting the db.sqlite3"
find . -path "*/db.sqlite3" -delete | tee

echo ">> deleting all *.py files under the migrations folder"
find . -path "*plm/migrations/*.py" -not -name "__init__.py" -delete | tee

echo ">> deleting all *.pyc files under the migrations folder"
find . -path "*plm/migrations/*.pyc" -delete | tee

echo ">> running makemigrations command..."
python manage.py makemigrations | tee

echo ">> running migrate command..."
python manage.py migrate | tee

echo ">> creating a superuser account with username admin and password admin"
echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', email='tamir@chipchop.com.au', password='admin')" | python manage.py shell

echo ">> creating some dummy test data"
python manage.py shell < scripts/create_dummy_data.py | tee

# chmod +x nuke_db.sh to make script executable