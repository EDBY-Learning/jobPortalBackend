from django.urls import path, include
from . import views


urlpatterns = [
    path('signup/',views.singupView.as_view(), name='signup'),
    path("demo/",views.demoView.as_view(),name='demo')
]
