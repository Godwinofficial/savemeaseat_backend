web: gunicorn backend.wsgi --timeout 9200 --keep-alive 9200 --log-file - 


worker: celery -A config worker --loglevel=info --pool=solo
beat: celery -A config beat --loglevel=info --scheduler django_celery_beat.schedulers:DatabaseScheduler