from django.db import models
from django.contrib.auth.models import Group, AbstractUser
from django.conf import settings
from django.urls import reverse

class Furnizor(models.Model):
    furnizor_id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Categorie(models.Model):
    STATUS_CHOICES = [
        ('activ', 'Activ'),
        ('inactiv', 'Inactiv'),
    ]

    categorie_id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='activ')
    icon = models.CharField(max_length=100, blank=True, null=True)
    culoare = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.name


class Produs(models.Model):
    produs_id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    stock_quantity = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    weight = models.FloatField()

    furnizor = models.ForeignKey(
        Furnizor,
        on_delete=models.CASCADE,
        related_name='produse'
    )

    categorie = models.ForeignKey(
        Categorie,
        on_delete=models.CASCADE,
        related_name='produse'
    )

    def __str__(self):
        return self.name


class Inventar(models.Model):
    MODIF_CHOICES = [
        ('buy', 'Buy'),   
        ('sell', 'Sell'), 
    ]

    inventar_id = models.BigAutoField(primary_key=True)

    produs = models.ForeignKey(
        Produs,
        on_delete=models.CASCADE,
        related_name='miscari_stoc'
    )
    

    cantitate = models.PositiveIntegerField(default=0)
    modif = models.CharField(max_length=4, choices=MODIF_CHOICES)
    date_modif = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        semn = '+' if self.modif == 'buy' else '-'
        return f"{self.produs.name} ({semn}{self.cantitate})"



class Promotie(models.Model):
    promotie_id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()

    # --- Relație M:N cu Produs ---
    produse = models.ManyToManyField(
        Produs,
        related_name='promotii'
    )
    

    def __str__(self):
        return f"{self.name} (-{self.discount_percentage}%)"
    
    def get_absolute_url(self):
        return reverse




class Ingredient(models.Model):
    ingredient_id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    benefit = models.CharField(max_length=200)
    protein_per_100g = models.DecimalField(max_digits=5, decimal_places=2)
    country_from = models.CharField(max_length=100)

    produse = models.ManyToManyField(
        Produs,
        related_name='ingrediente'
    )
    

    def __str__(self):
        return self.name


class Organizator(models.Model):
    organizator_id = models.BigAutoField(primary_key=True)
    nume = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return self.nume


class Locatie(models.Model):
    locatie_id = models.BigAutoField(primary_key=True)
    adresa = models.CharField(max_length=255)
    oras = models.CharField(max_length=100)
    judet = models.CharField(max_length=100)
    cod_postal = models.CharField(max_length=10)
    nr = models.IntegerField()

    def __str__(self):
        return f"{self.adresa}, {self.oras}"
    
#####NOILE
class User(AbstractUser):
    nr_tel = models.CharField(max_length=15, blank=True, null=True)
    data_nasterii = models.DateField(blank=True, null=True)
    vip = models.BooleanField(default=False)
    adresa = models.CharField(max_length=200, blank=True, null=True)
    tara = models.CharField(max_length=20, blank=True, null=True)
    cod = models.CharField(max_length=100, null=True, blank=True)
    email_confirmat = models.BooleanField(default=False)
    blocat = models.BooleanField(default=False)


    def __str__(self):
        return self.username



class Comanda(models.Model):
    TIP_AMBALAJ_CHOICES = [
        ('cutie', 'Cutie'),
        ('plic', 'Plic'),
        ('palet', 'Palet'),
    ]

    comanda_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    valoare = models.DecimalField(max_digits=7, decimal_places=2)
    tip_ambalaj = models.CharField(max_length=20, choices=TIP_AMBALAJ_CHOICES)
    curier = models.CharField(max_length=20)
    produse = models.ManyToManyField('Produs', related_name='comenzi')

    def __str__(self):
        return f"Comanda #{self.comanda_id} - {self.user.username}"



class PuncteFidelitate(models.Model):
    id_puncte = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    data_comenzii = models.DateField()
    data_revendicarii = models.DateField(blank=True, null=True)
    multiplicator = models.DecimalField(max_digits=3, decimal_places=1)
    puncte_castigate = models.IntegerField(default=0)

    def __str__(self):
        return f"Puncte {self.user.username} - {self.puncte_castigate}"


class Review(models.Model):
    review_id = models.AutoField(primary_key=True)
    produs = models.ForeignKey(Produs, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tip = models.CharField(max_length=20)
    mesaj = models.CharField(max_length=300)

    def __str__(self):
        return f"Review de la {self.user.username} pentru {self.produs.name}"



class Vizualizare(models.Model):
    id_viz = models.AutoField(primary_key=True)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    produs = models.ForeignKey(Produs, on_delete=models.CASCADE)
    data_vizualizare = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} a vizualizat {self.produs.name}"


class PromotieNoua(models.Model):
    id_promotie = models.AutoField(primary_key=True)

    nume = models.CharField(max_length=100)
    data_creare = models.DateField(auto_now_add=True)
    data_expirare = models.DateField()

    reducere = models.IntegerField(default=10)  #1   
    descriere = models.TextField()               #2 

    categorii = models.ManyToManyField(Categorie)

    def __str__(self):
        return f"Promoție: {self.nume}"
    

