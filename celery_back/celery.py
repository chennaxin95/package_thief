from celery import Celery

app = Celery('celery_back', borker='redis://package_thief@localhost:6379',
            task_serializer='pickle', result_serializer='pickle')

app.conf.task_serializer = 'pickle'
app.conf.result_serializer = 'pickle'

if __name__=='__main__':
    app.start()
