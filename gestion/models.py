from datetime import timedelta

from django.db import models
from django.utils import timezone


class Media(models.Model):
    """Classe mère de tous les médias empruntables."""
    name = models.CharField(max_length=200)
    disponible = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Livre(Media):
    auteur = models.CharField(max_length=100)


class Dvd(Media):
    realisateur = models.CharField(max_length=100)


class Cd(Media):
    artiste = models.CharField(max_length=100)


class JeuDePlateau(models.Model):
    """Consultation uniquement : ce n'est PAS un Media empruntable."""
    name = models.CharField(max_length=200)
    createur = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Membre(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.prenom} {self.nom}"

    def emprunts_en_cours(self):
        """Emprunts pas encore rendus."""
        return self.emprunt_set.filter(date_retour_effective__isnull=True)

    def est_bloque(self):
        """Bloqué s'il a un emprunt en cours dont la date prévue est dépassée."""
        return self.emprunts_en_cours().filter(
            date_retour_prevue__lt=timezone.localdate()
        ).exists()

    def peut_emprunter(self):
        """Vrai si pas bloqué et moins de 3 emprunts en cours."""
        return not self.est_bloque() and self.emprunts_en_cours().count() < 3


class Emprunt(models.Model):
    media = models.ForeignKey(Media, on_delete=models.PROTECT)
    membre = models.ForeignKey(Membre, on_delete=models.CASCADE)
    date_emprunt = models.DateField(default=timezone.localdate)
    date_retour_prevue = models.DateField(blank=True)
    date_retour_effective = models.DateField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.date_retour_prevue:
            self.date_retour_prevue = self.date_emprunt + timedelta(days=7)
        super().save(*args, **kwargs)

    def est_en_retard(self):
        return (
            self.date_retour_effective is None
            and self.date_retour_prevue < timezone.localdate()
        )