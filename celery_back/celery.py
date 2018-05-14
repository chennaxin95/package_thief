from celery import Celery

app = Celery('celery_back', borker='redis://package_thief@localhost:6379')

if __name__=='__main__':
    app.start()
