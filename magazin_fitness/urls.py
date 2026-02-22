"""
URL configuration for magazin_fitness project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from magazin_app import views
from magazin_app.sitemaps import ProdusSitemap, CategorieSitemap, StaticViewSitemap, promotie_generic_sitemap
from django.contrib.sitemaps.views import sitemap

sitemaps = {
    'produse': ProdusSitemap,
    'categorii': CategorieSitemap,
    'statice': StaticViewSitemap,
    'promotii': promotie_generic_sitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('magazin_app.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemap'),
]
