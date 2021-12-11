from django.urls import path
from . import views

urlpatterns = [
    path('', views.satelliteDetail, name="satellite"),
    path('overview/', views.apiOverview, name="api-overview"),
    path('all/', views.satelliteList, name="satellites"),
    path('search/', views.satelliteSearch, name="satellitesSearch"),
    path('page=<int:number>/', views.satellitePage, name="satellitesPage"),
    path('create/', views.satelliteCreate, name="satellite-create"),
    path('update/', views.satelliteUpdate, name="satellite-update"),
    path('delete/', views.satelliteDelete, name="satellite-delete"),
    path('visible/', views.satelliteVisibility, name="satellite-visible"),
]