from django.urls import path
from .views import health, add_job_by_outsider,add_job,get_all_jobs,get_jobs,login_user,logout_user,\
user_next_page,get_latest_jobs,get_data_for_vis,get_job_by_id,get_job_by_ids,add_feedback_by_user

urlpatterns = [
    path('job_portal_health',health),
    path('add_job',add_job),
    path('add_job_by_outsider',add_job_by_outsider),
    path('get_all_jobs',get_all_jobs),
    path('get_jobs',get_jobs),
    path('login',login_user),
    path('logout',logout_user),
    path('user_next_page',user_next_page),
    path('get_latest_jobs',get_latest_jobs),
    path('get_data_for_vis',get_data_for_vis),
    path('jobbyid',get_job_by_id),
    path('jobbyids',get_job_by_ids),
    path('add_feedback_by_user',add_feedback_by_user),
]