from django import forms
from .models import Membre, Media, Livre, Dvd, Cd, JeuDePlateau, Emprunt


class MembreForm(forms.ModelForm):
    class Meta:
        model = Membre
        fields = ['nom', 'prenom']


class LivreForm(forms.ModelForm):
    class Meta:
        model = Livre
        fields = ['name', 'auteur']


class DvdForm(forms.ModelForm):
    class Meta:
        model = Dvd
        fields = ['name', 'realisateur']


class CdForm(forms.ModelForm):
    class Meta:
        model = Cd
        fields = ['name', 'artiste']


class JeuDePlateauForm(forms.ModelForm):
    class Meta:
        model = JeuDePlateau
        fields = ['name', 'createur']


class EmpruntForm(forms.ModelForm):
    class Meta:
        model = Emprunt
        fields = ['media', 'membre']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # On ne propose que les médias disponibles
        self.fields['media'].queryset = Media.objects.filter(disponible=True)

    def clean(self):
        cleaned_data = super().clean()
        membre = cleaned_data.get('membre')
        if membre is not None:
            if membre.est_bloque():
                raise forms.ValidationError(
                    "Ce membre a un emprunt en retard : il ne peut plus emprunter."
                )
            if not membre.peut_emprunter():
                raise forms.ValidationError(
                    "Ce membre a déjà 3 emprunts en cours."
                )
        return cleaned_data
