from django.contrib import admin
from .models import Media, Livre, Dvd, Cd, JeuDePlateau, Membre, Emprunt

admin.site.register([Media, Livre, Dvd, Cd, JeuDePlateau, Membre, Emprunt])