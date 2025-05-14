python -m venv venv
. venv/scripts/activate
pip install --upgrade pip
pip install -r requirements.txt

django-admin startproject review_service
python manage.py startapp accounts
python manage.py startapp dashboard
python manage.py startapp reviews

mkdir -p reviews/management/commands
touch reviews/management/__init__.py
touch reviews/management/commands/__init__.py
touch reviews/management/commands/generate_reviews.py

python manage.py generate_reviews
