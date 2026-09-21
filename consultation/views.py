from django.views.generic import ListView

from gestion.models import Media, JeuDePlateau


class CatalogueView(ListView):
    """Liste de tous les médias, en lecture seule."""
    model = Media
    template_name = 'consultation/catalogue.html'
    context_object_name = 'medias'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['jeux'] = JeuDePlateau.objects.all()
        return context
