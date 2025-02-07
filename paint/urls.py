from django.urls import path
from . import views
from django.contrib.auth import views as auth_view


urlpatterns = [
    path('',views.home, name='home'),
    path('signin/', views.signin, name='signin'),
    path('signout/', views.signout, name='signout'),
    path('register/', views.register, name='register'),
    path('update_password/',auth_view.PasswordChangeView.as_view(template_name="update_password.html",success_url="/user_dashboard/" ),name='update_password'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard')
]