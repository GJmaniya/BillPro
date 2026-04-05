from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.user_login, name='login'),
    path('register/', views.user_register, name='register'),
    path('logout/', views.user_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('bill/create/', views.create_bill, name='create_bill'),
    path('bill/<int:id>/download/', views.download_bill, name='download_bill'),
    path('bill/<int:id>/whatsapp/', views.whatsapp_share, name='whatsapp_share'),
    path('challan/create/', views.create_challan, name='create_challan'),
    path('challan/<int:id>/download/', views.download_challan, name='download_challan'),
]
