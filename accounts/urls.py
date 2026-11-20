from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('deposit/', views.deposit_view, name='deposit'),
    path('withdraw/', views.withdraw_view, name='withdraw'),
    path('transactions/', views.transaction_history_view, name='transactions'),
]