from celery import Celery # pip install celery redis

# Configure Celery with a Redis broker
def make_celery(app):
    celery = Celery(
        app.import_name,
        backend='redis://localhost:6379/0',
        broker='redis://localhost:6379/0'
    )
    celery.conf.update(app.config)
    return celery

# redis-server
# python main.py
# celery -A main.celery worker --loglevel=info
# python computer_vision.py



