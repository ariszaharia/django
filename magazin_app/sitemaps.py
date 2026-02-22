from django.contrib.sitemaps import Sitemap, GenericSitemap
from django.urls import reverse
from .models import Produs, Categorie, Promotie


class ProdusSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Produs.objects.filter(is_active=True)

    def location(self, obj):
        return reverse("produs_detalii", args=[obj.produs_id])


class CategorieSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.6

    def items(self):
        return Categorie.objects.all()

    def location(self, obj):
        return reverse("categorie_detalii", args=[obj.name.lower()])


class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = "weekly"

    def items(self):
        return [
            "index",
            "produse",
            "contact",
            "despre",
            "register",
            "login",
        ]

    def location(self, item):
        return reverse(item)

promotie_dict = {
    "queryset": Promotie.objects.all(),
}

promotie_generic_sitemap = GenericSitemap(promotie_dict, priority=0.7)
