from uuid import uuid4
from datetime import datetime, timedelta
import os
from .models import JobInfo, JobPostByOutSider

from datetime import datetime, timedelta
from django.conf import settings as conf_settings
import pytz

BACKEND_TIME_ZONE = pytz.timezone(conf_settings.TIME_ZONE)




@background(schedule=10)
def delete_data_periodically(seconds=10):
    # lookup user by id and send them a message
    #seconds=10
    print("running scheduled task")
    #seconds = 20
    time_in_days = seconds/60/60/24
    JobPostByOutSider.objects.filter(entry_time__lte=datetime.now().astimezone(BACKEND_TIME_ZONE)-timedelta(days=time_in_days)).delete()

delete_data_periodically(10,repeat=10)
