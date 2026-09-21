# Rapport : logiciel de gestion de médiathèque

## 1. Étude et correctifs du code fourni
- Classes en minuscules (`livre`, `dvd`) : renommées en CamelCase (PEP 8).
- Attributs de classe sans `__init__` : remplacés par des models Django (champs typés).
- Duplication de `name`, `dateEmprunt`, `disponible`, `emprunteur` : factorisée dans une classe mère `Media` dont héritent `Livre`, `Dvd`, `Cd`.
- Mauvais types (`disponible = ""`, `dateEmprunt = ""`) : `BooleanField` et `DateField`.
- `emprunteur` en texte : remplacé par une classe `Emprunt` reliant `Membre` et `Media`.
- Attribut `bloque` : supprimé, calculé par `Membre.est_bloque()` (emprunt en retard).
- `Emprunteur` renommé `Membre`.
- Menus en `print` : remplacés par des pages web Django.
- Aucune persistance : PostgreSQL protégé par mot de passe.
- Conservé : l'idée des classes Livre, Dvd, Cd, JeuDePlateau et la séparation appli bibliothécaire / appli membre.

## 2. Fonctionnalités
- Application `gestion` (bibliothécaires, `/bibliotheque/`) : créer, lister, modifier, supprimer un membre ; lister et ajouter des médias ; créer un emprunt ; rentrer un emprunt.
- Application `consultation` (membres, `/`) : liste en lecture seule des médias et des jeux.
- Règles métier dans `models.py` (`peut_emprunter`, `est_bloque`, retour à 7 jours) et appliquées dans `EmpruntForm.clean()` (style défensif).
- `JeuDePlateau` n'hérite pas de `Media` : l'emprunt est impossible par construction.
- `transaction.atomic()` garde l'emprunt et la disponibilité cohérents.
- Logs : configuration `LOGGING` (console + fichier `mediatheque.log`).
- Correctif en cours de route : `date_retour_prevue` en `blank=True` et `timezone.localdate` pour la date d'emprunt.

## 3. Stratégie de tests
13 tests Django (`gestion/tests.py`), au moins un par fonctionnalité : CRUD des membres, ajout et liste des médias, création et retour d'emprunt, retour à 7 jours, limite de 3 emprunts, blocage en cas de retard, catalogue public. Lancement : `python manage.py test`.

## 4. Base de données de test
Fichier `gestion/fixtures/donnees_test.json` : 3 membres, 3 livres, 1 DVD, 1 CD, 2 jeux, un emprunt en cours et un emprunt en retard. Chargement : `python manage.py loaddata donnees_test`.

## 5. Exécution depuis une autre machine
Prérequis : Python 3.10+, Docker.
1. `git clone <URL_DU_REPO>` puis `cd mediatheque`
2. `python -m venv venv` puis `source venv/bin/activate` (Windows : `venv\Scripts\activate`)
3. `pip install -r requirements.txt`
4. `cp .env.example .env` puis choisir un mot de passe dans `.env`
5. `docker compose up -d`
6. `python manage.py migrate`
7. `python manage.py loaddata donnees_test`
8. `python manage.py runserver`
9. Bibliothécaires : http://127.0.0.1:8000/bibliotheque/membres/ ; membres : http://127.0.0.1:8000/

## 6. Limite connue
Quand on supprime un membre, ses emprunts sont supprimés avec lui (`on_delete=CASCADE`), mais les médias encore empruntés ne repassent pas automatiquement en « Disponible ». Une amélioration possible serait de les remettre disponibles avant la suppression, ou d'interdire la suppression d'un membre qui a des emprunts en cours.
