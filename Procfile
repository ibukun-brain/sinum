web: daphne sinum.routing:application --port $PORT --bind 0.0.0.0 -v2
celery: celery --app=sinum worker -E
worker: python manage.py runworker channels --settings=sinum.production_settings -v2
# beat: celery -A reportr beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
