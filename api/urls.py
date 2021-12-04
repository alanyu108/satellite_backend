from django.urls import path
from . import views

urlpatterns = [
    path('', views.apiOverview, name="api-overview"),
    path('satellites/', views.satelliteList, name="satellites"),
    path('satellites/search/', views.satelliteSearch, name="satellitesSearch"),
    path('satellites/page=<int:number>/', views.satellitePage, name="satellitesPage"),
    path('satellite/', views.satelliteDetail, name="satellite"),
    path('satellite-create/', views.satelliteCreate, name="satellite-create"),
    path('satellite-update/', views.satelliteUpdate, name="satellite-update"),
    path('satellite-delete/', views.satelliteDelete, name="satellite-delete"),
    path('satellite-visible/', views.satelliteVisibility, name="satellite-visible"),
]