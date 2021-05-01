from django.dispatch import Signal
from django.dispatch import receiver

from .models import SearchCRM


job_search_signal = Signal(providing_args=["username","result_count","subjects","city","positions"])

@receiver(job_search_signal, sender=None)
def handle_job_search_signal(sender, **kwargs):
    data_keys = ["username","result_count","subjects","city","positions"]
    data = {key:kwargs.get(key,"") for key in data_keys}        
    print(data)
    print(kwargs)
    obj = SearchCRM.objects.create(**data)
    obj.save()



