from django.urls import path, include
from . import views
urlpatterns = [
    path("", views.index, name='index'),
    path("info/", views.info, name="info"),
    path("exemplu/" , views.afis_template, name="exemplu"),
    path("log/", views.log, name="log"),
    path("contact/", views.contact, name="contact"),
    path("produse/", views.produse, name="produse"),
    path("cos/", views.cos, name="cos"),
    path("despre/", views.despre, name="despre"),
    path("locatii/", views.afis_produse, name="locatii"),\
    path("produse/<int:produs_id>/", views.afis_produse, name="produs_detalii"),
    path("categorii/<str:nume_categorie>/", views.categorie_detalii, name="categorie_detalii"),
    path("categorii/", views.categorie, name = "categorii"),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('password/', views.change_password_view, name='change_password'),
    path("add/", views.adauga_produs, name = "adauga_produs"),
    path('confirma_mail/<str:cod>/', views.confirma_mail, name='confirma_mail'),
    path("promotii/", views.promotii_view, name="promotii"),
    path("interzis/", views.pagina_interzisa, name="pagina_interzisa"),
    path("activeaza_oferta/", views.activeaza_oferta, name="activeaza_oferta"),
    path("oferta/", views.oferta, name="oferta"),
    path("finalizeaza_comanda/", views.finalizeaza_comanda, name="finalizeaza_comanda"),
    path("actualizeaza_date/", views.actualizeaza_date, name="actualizeaza_date"),
]

