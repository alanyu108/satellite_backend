from django.urls import path
from . import views

urlpatterns = [
    path('', views.debrisDetail, name="debris"),
    path('all/', views.debrisList, name="debris-all"),
    path('create/', views.debrisCreate, name="debris-create"),
    path('update/', views.debrisUpdate, name="debris-update"),
    path('delete/', views.debrisDelete, name="debris-delete"),
    path('search/', views.debrisSearch, name="debris-search"),
    path('page=<int:number>/', views.debrisPage, name="debris-page"),
]