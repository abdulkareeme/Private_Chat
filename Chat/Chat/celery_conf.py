from celery import Celery
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Chat.settings')

app = Celery('Chat')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.task_routes = {
        'conversation.tasks.send_notification_task':{"queue":"notification_queue"},
        'conversation.tasks.send_periodic_message':{'queue':'periodic_message'},
        'core.tasks.send_email_confirmation':{'queue':'email_confirmation'}
    }

app.conf.task_default_rate_limit = '100/m'

app.conf.broker_transport_options = {  # for priority for redis
    'priority_steps': list(range(10)),
    'sep': ':',
    'queue_order_strategy': 'priority'
}
app.autodiscover_tasks()