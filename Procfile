release: python manage.py migrate
web: gunicorn fitbit.wsgi --log-file=-
worker: celery -A datauploader worker --concurrency 1
