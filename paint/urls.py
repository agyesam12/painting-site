from django.urls import path
from . import views
from django.contrib.auth import views as auth_view


urlpatterns = [
    path('',views.home, name='home'),
    path('signin/', views.signin, name='signin'),
    path('signout/', views.signout, name='signout'),
    path('register/', views.register, name='register'),
    path('update_password/',auth_view.PasswordChangeView.as_view(template_name="update_password.html",success_url="/user_dashboard/" ),name='update_password'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
     path('create_service/', views.create_service, name='create_service'),
    path('create_portfolio/', views.create_portfolio, name='create_portfolio'),
    path('create_testimonial/', views.create_testimonial, name='create_testimonial'),
]