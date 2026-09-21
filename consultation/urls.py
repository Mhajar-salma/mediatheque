from django.urls import path
from . import views

urlpatterns = [
    path('', views.CatalogueView.as_view(), name='catalogue'),
]
