from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Membre, Media, Livre, JeuDePlateau, Emprunt


def creer_membre(nom='Dupont', prenom='Marie'):
    return Membre.objects.create(nom=nom, prenom=prenom)


def creer_livre(titre='Livre test'):
    return Livre.objects.create(name=titre, auteur='Auteur')


class MembreTests(TestCase):
    def test_creer_membre(self):
        self.client.post(reverse('membre_create'), {'nom': 'Dupont', 'prenom': 'Marie'})
        self.assertEqual(Membre.objects.count(), 1)

    def test_liste_membres(self):
        creer_membre()
        reponse = self.client.get(reverse('membre_list'))
        self.assertContains(reponse, 'Marie Dupont')

    def test_modifier_membre(self):
        membre = creer_membre()
        self.client.post(
            reverse('membre_update', args=[membre.pk]),
            {'nom': 'Martin', 'prenom': 'Marie'},
        )
        membre.refresh_from_db()
        self.assertEqual(membre.nom, 'Martin')

    def test_supprimer_membre(self):
        membre = creer_membre()
        self.client.post(reverse('membre_delete', args=[membre.pk]))
        self.assertEqual(Membre.objects.count(), 0)


class MediaTests(TestCase):
    def test_ajouter_livre(self):
        self.client.post(reverse('livre_create'), {'name': 'Dune', 'auteur': 'Herbert'})
        self.assertEqual(Livre.objects.count(), 1)

    def test_liste_medias(self):
        creer_livre('Dune')
        reponse = self.client.get(reverse('media_list'))
        self.assertContains(reponse, 'Dune')

    def test_jeu_de_plateau_pas_empruntable(self):
        JeuDePlateau.objects.create(name='Catan', createur='Teuber')
        self.assertEqual(Media.objects.count(), 0)


class EmpruntTests(TestCase):
    def test_creer_emprunt(self):
        membre = creer_membre()
        livre = creer_livre()
        self.client.post(reverse('emprunt_create'), {'media': livre.pk, 'membre': membre.pk})
        self.assertEqual(Emprunt.objects.count(), 1)
        livre.refresh_from_db()
        self.assertFalse(livre.disponible)

    def test_retour_d_un_emprunt(self):
        membre = creer_membre()
        livre = creer_livre()
        self.client.post(reverse('emprunt_create'), {'media': livre.pk, 'membre': membre.pk})
        emprunt = Emprunt.objects.get()
        self.client.post(reverse('emprunt_retour', args=[emprunt.pk]))
        emprunt.refresh_from_db()
        livre.refresh_from_db()
        self.assertIsNotNone(emprunt.date_retour_effective)
        self.assertTrue(livre.disponible)

    def test_retour_prevu_a_une_semaine(self):
        emprunt = Emprunt.objects.create(media=creer_livre(), membre=creer_membre())
        self.assertEqual(
            emprunt.date_retour_prevue, emprunt.date_emprunt + timedelta(days=7)
        )

    def test_maximum_3_emprunts(self):
        membre = creer_membre()
        for i in range(3):
            Emprunt.objects.create(media=creer_livre(f'L{i}'), membre=membre)
        quatrieme = creer_livre('L4')
        self.client.post(reverse('emprunt_create'), {'media': quatrieme.pk, 'membre': membre.pk})
        self.assertEqual(Emprunt.objects.count(), 3)

    def test_membre_en_retard_bloque(self):
        membre = creer_membre()
        vieille_date = timezone.localdate() - timedelta(days=10)
        Emprunt.objects.create(media=creer_livre('Ancien'), membre=membre, date_emprunt=vieille_date)
        self.assertTrue(membre.est_bloque())
        nouveau = creer_livre('Nouveau')
        self.client.post(reverse('emprunt_create'), {'media': nouveau.pk, 'membre': membre.pk})
        self.assertEqual(Emprunt.objects.count(), 1)


class ConsultationTests(TestCase):
    def test_catalogue_public(self):
        creer_livre('Dune')
        JeuDePlateau.objects.create(name='Catan', createur='Teuber')
        reponse = self.client.get(reverse('catalogue'))
        self.assertContains(reponse, 'Dune')
        self.assertContains(reponse, 'Catan')
