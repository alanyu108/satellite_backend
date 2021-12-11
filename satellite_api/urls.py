from django.urls import path
from . import views

urlpatterns = [
    path('overview/', views.satelliteOverview, name="satellite-overview"),
    path('', views.satelliteDetail, name="satellite"),
    path('all/', views.satelliteList, name="satellite-all"),
    path('search/', views.satelliteSearch, name="satellite-search"),
    path('page=<int:number>/', views.satellitePage, name="satellites-page"),
    path('create/', views.satelliteCreate, name="satellite-create"),
    path('update/', views.satelliteUpdate, name="satellite-update"),
    path('delete/', views.satelliteDelete, name="satellite-delete"),
    path('visible/', views.satelliteVisibility, name="satellite-visible"),
]