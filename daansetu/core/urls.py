from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .forms import CustomAuthenticationForm

urlpatterns = [
    # Common pages
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    
    # Donor pages
    path('donor/dashboard/', views.donor_dashboard, name='donor_dashboard'),
    path('donor/donate/item/', views.donate_item, name='donate_item'),
    path('donor/donate/money/', views.donate_money, name='donate_money'),
    path('donor/history/', views.donation_history, name='donation_history'),
    
    # Volunteer pages
    path('volunteer/dashboard/', views.volunteer_dashboard, name='volunteer_dashboard'),
    path('volunteer/tasks/', views.volunteer_tasks, name='volunteer_tasks'),
    path('volunteer/task/<int:assignment_id>/complete/', views.complete_task, name='complete_task'),
    path('volunteer/donation/<int:donation_id>/accept/', views.accept_donation, name='accept_donation'),
    
    # Admin pages - change prefix to daansetu_admin to avoid conflict with Django admin
    path('daansetu_admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('daansetu_admin/users/', views.admin_users, name='admin_users'),
    path('daansetu_admin/donations/', views.admin_donations, name='admin_donations'),
    path('daansetu_admin/assign/volunteer/', views.assign_volunteer, name='assign_volunteer'),
]
