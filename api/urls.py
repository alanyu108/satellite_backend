from django.urls import path
from . import views

urlpatterns = [
    path('', views.apiOverview, name="api-overview"),
    path('satellites/', views.satelliteList, name="satellites"),
    path('satellite/<str:primaryKey>/', views.satelliteDetail, name="satellite"),
    path('satellite-create/', views.satelliteCreate, name="satellite-create"),
    path('satellite-update/<str:primaryKey>/', views.satelliteUpdate, name="satellite-update"),
    path('satellite-delete/<str:primaryKey>/', views.satelliteDelete, name="satellite-delete"),
]