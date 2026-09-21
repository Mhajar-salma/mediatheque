from django.urls import path
from . import views

urlpatterns = [
    path('membres/', views.MembreListView.as_view(), name='membre_list'),
    path('membres/nouveau/', views.MembreCreateView.as_view(), name='membre_create'),
    path('membres/<int:pk>/modifier/', views.MembreUpdateView.as_view(), name='membre_update'),
    path('membres/<int:pk>/supprimer/', views.MembreDeleteView.as_view(), name='membre_delete'),
    path('medias/', views.MediaListView.as_view(), name='media_list'),
    path('medias/livre/nouveau/', views.LivreCreateView.as_view(), name='livre_create'),
    path('medias/dvd/nouveau/', views.DvdCreateView.as_view(), name='dvd_create'),
    path('medias/cd/nouveau/', views.CdCreateView.as_view(), name='cd_create'),
    path('jeux/nouveau/', views.JeuDePlateauCreateView.as_view(), name='jeu_create'),
    path('emprunts/', views.EmpruntListView.as_view(), name='emprunt_list'),
    path('emprunts/nouveau/', views.EmpruntCreateView.as_view(), name='emprunt_create'),
    path('emprunts/<int:pk>/retour/', views.EmpruntRetourView.as_view(), name='emprunt_retour'),
]
