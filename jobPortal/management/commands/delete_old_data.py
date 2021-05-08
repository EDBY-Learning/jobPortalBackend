from django.core.management.base import BaseCommand
from django.utils.crypto import get_random_string
from jobPortal.models import JobInfo, JobPostByOutSider
from datetime import datetime, timedelta
from django.conf import settings as conf_settings
import pytz

BACKEND_TIME_ZONE = pytz.timezone(conf_settings.TIME_ZONE)
class Command(BaseCommand):
    help = 'Create random users'

    def add_arguments(self, parser):
        parser.add_argument('-dbname', type=str, help='Name of databse')
        parser.add_argument('-days', type=float, help='Time in days (can be float)')

    def handle(self, *args, **kwargs):
        db = kwargs['dbname']
        time_in_days = kwargs['days']
        if db=='JobInfo':
            JobInfo.objects.filter(entry_time__lte=datetime.now().astimezone(BACKEND_TIME_ZONE)-timedelta(days=time_in_days)).delete()
        elif db=='JobPostByOutSider':
            print(BACKEND_TIME_ZONE)
            JobPostByOutSider.objects.filter(entry_time__lte=datetime.now().astimezone(BACKEND_TIME_ZONE)-timedelta(days=time_in_days)).delete()
        else:
            print("No such table exists ",db)
        
    #example
    #python manage.py delete_old_data -dbname=JobPostByOutSider -days=.001