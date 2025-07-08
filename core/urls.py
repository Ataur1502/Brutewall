from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('export/csv/', views.export_logs_csv, name='export_csv'),
    path('reset/<str:ip_address>/', views.reset_ip, name='reset_ip'),

]
