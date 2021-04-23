from django.urls import path, include
from .views import Details,Health

urlpatterns = [
    path("threads_num/",Details.as_view()),
    path("health/",Health.as_view())
]
