from django.urls import path
from . import views
from .views import *
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
    path('book_us/', views.book_us, name='book_us'),
    path('booking_requests', views.booking_requests, name='booking_requests'),
    path('portfolio_lists', views.portfolio_lists, name='portfolio_lists'),
    path('UpdatePortfolio/<int:portfolio_id>/', UpdatePortfolio.as_view(), name='update_portfolio'),
    path('portfolio/datail/<int:portfolio_id>/',PortfolioDetailView.as_view(),name='portfolio_detail'),
    path('DisplayNotifications/', DisplayNotifications.as_view(), name='DisplayNotifications'),
    path('mark-notification-read/<int:notification_id>/', views.mark_notification_read, name='mark_notification_read'),
    path('display_notifications', views.display_notifications, name='display_notifications'),
    path('portfolios_page/', DisplayPortfolios.as_view(), name='portfolios_page'),
    path('portfolio/delete/<int:portfolio_id>', PortfolioDeleteView.as_view(), name='delete_portfolio'),
]