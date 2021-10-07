from django.urls import path
from . import views

urlpatterns = [
    path('', views.apiOverview, name="api-overview"),
    path('satellites/', views.satelliteList, name="satellites"),
    path('satellite/<str:parameter>/', views.satelliteDetail, name="satellite"),
    path('satellite-create/', views.satelliteCreate, name="satellite-create"),
    path('satellite-update/<str:parameter>/', views.satelliteUpdate, name="satellite-update"),
    path('satellite-delete/<str:parameter>/', views.satelliteDelete, name="satellite-delete"),
]