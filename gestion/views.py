import logging

from django.db import transaction
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .forms import (
    MembreForm, LivreForm, DvdForm, CdForm, JeuDePlateauForm, EmpruntForm,
)
from .models import Membre, Media, Livre, Dvd, Cd, JeuDePlateau, Emprunt

logger = logging.getLogger(__name__)


class MembreListView(ListView):
    model = Membre
    template_name = 'gestion/membre_list.html'
    context_object_name = 'membres'


class MembreCreateView(CreateView):
    model = Membre
    form_class = MembreForm
    template_name = 'gestion/membre_form.html'
    success_url = reverse_lazy('membre_list')

    def form_valid(self, form):
        logger.info("Membre créé : %s", form.cleaned_data)
        return super().form_valid(form)


class MembreUpdateView(UpdateView):
    model = Membre
    form_class = MembreForm
    template_name = 'gestion/membre_form.html'
    success_url = reverse_lazy('membre_list')


class MembreDeleteView(DeleteView):
    model = Membre
    template_name = 'gestion/membre_confirm_delete.html'
    success_url = reverse_lazy('membre_list')


class MediaListView(ListView):
    model = Media
    template_name = 'gestion/media_list.html'
    context_object_name = 'medias'


class LivreCreateView(CreateView):
    model = Livre
    form_class = LivreForm
    template_name = 'gestion/media_form.html'
    success_url = reverse_lazy('media_list')


class DvdCreateView(CreateView):
    model = Dvd
    form_class = DvdForm
    template_name = 'gestion/media_form.html'
    success_url = reverse_lazy('media_list')


class CdCreateView(CreateView):
    model = Cd
    form_class = CdForm
    template_name = 'gestion/media_form.html'
    success_url = reverse_lazy('media_list')


class JeuDePlateauCreateView(CreateView):
    model = JeuDePlateau
    form_class = JeuDePlateauForm
    template_name = 'gestion/media_form.html'
    success_url = reverse_lazy('media_list')


class EmpruntListView(ListView):
    model = Emprunt
    template_name = 'gestion/emprunt_list.html'
    context_object_name = 'emprunts'


class EmpruntCreateView(CreateView):
    model = Emprunt
    form_class = EmpruntForm
    template_name = 'gestion/emprunt_form.html'
    success_url = reverse_lazy('emprunt_list')

    def form_valid(self, form):
        with transaction.atomic():
            response = super().form_valid(form)
            media = self.object.media
            media.disponible = False
            media.save()
        logger.info("Emprunt créé : %s par %s", self.object.media, self.object.membre)
        return response


class EmpruntRetourView(View):
    """Rentrer un emprunt : POST uniquement."""

    def post(self, request, pk):
        emprunt = get_object_or_404(
            Emprunt, pk=pk, date_retour_effective__isnull=True
        )
        with transaction.atomic():
            emprunt.date_retour_effective = timezone.localdate()
            emprunt.save()
            emprunt.media.disponible = True
            emprunt.media.save()
        logger.info("Emprunt rendu : %s par %s", emprunt.media, emprunt.membre)
        return redirect('emprunt_list')
