from django.urls import path, include
from . import views
import os

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

from rest_framework.routers import DefaultRouter, SimpleRouter
#from rest_framework.urlpatterns import format_suffix_patterns

if os.environ.get('ENV')=='local' and bool(int(os.environ.get("DEBUG",0)))==True:
    router = DefaultRouter()
else:
    router = SimpleRouter()
router.register(r'change_password',views.ChangePasswordViewSet,basename='change_password')
router.register(r'reset_password_with_token',views.ChangeForgetPasswordViewSet,basename='reset_password_with_token')

urlpatterns = [
    path('',include(router.urls)),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login_admin/',views.AdminTokenObtainPairView.as_view(), name='admin_token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('login/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('logout/', TokenRefreshView.as_view(), name='token_delete'),
    path('get_reset_password_token/',views.ForgetPasswordView.as_view(), name='get_reset_password_token'),
    path("save_forgot_password_data/",views.SaveForgotPasswordData.as_view(),name='save_forgot_password_data')

]
