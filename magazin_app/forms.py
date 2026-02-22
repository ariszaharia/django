from django import forms
from django.core.exceptions import ValidationError
from datetime import date, datetime
import re
from .models import User, Categorie, Produs
from django.contrib.auth import get_user_model
import string
import secrets
from django.contrib.auth.forms import AuthenticationForm
# Validatori personalizati

def validate_cnp(value):
    if len(value)!= 13:
        raise ValidationError("CNP-ul trebuie sa contina exact 13 cifre.")
    if value[0] not in ['1', '2', '5', '6']:
        raise ValidationError("CNP-ul trebuie sa inceapa cu 1 sau 2.")
    try:
        anul = int(value[1:3])
        luna = int(value[3:5])
        zi = int(value[5:7])
        anul += 1900 if value[0] in ['1', '2'] else 2000
        datetime(anul, luna, zi)  
    except ValueError:
        raise ValidationError("CNP invalid")

def validate_major(value):
    today = date.today()
    age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
    if age < 18:
        raise ValidationError("Trebuie sa aveti peste 18 ani pentru a trimite formularul.")

def validate_capital_clean(value):
    if not re.match(r'^[A-Z][a-zA-Z\s-]*$', value):
        raise ValidationError(
            "Textul trebuie sa inceapa cu litera mare si sa contina doar litere, spatii sau cratime."
        )

def validate_capital_after_space(value):
    parts = value.split()
    for part in parts:
        if part and not part[0].isupper():
            raise ValidationError("Fiecare cuvant trebuie sa inceapa cu litera mare.")
        

def validate_email_temp(value):
    domenii_interzise = ["guerillamail.com", "yopmail.com"]
    domeniu = value.split("@")[-1].lower()
    if domeniu in domenii_interzise:
        raise ValidationError("Adresa de email nu poate fi temporara (ex: guerillamail, yopmail).")
    

def validate_message(value):
    if not re.fullmatch(r"[A-Za-z\s-]+", value):
        raise ValidationError("Mesajul poate contine doar litere, spatii si cratime.")

    words = re.findall(r"[A-Za-z]+", value)

    if not (5 <= len(words) <= 100):
        raise ValidationError("Mesajul trebuie să contina între 5 si 100 de cuvinte.")

    for w in words:
        if len(w) > 15:
            raise ValidationError("Niciun cuvant nu poate depasi 15 caractere.")

def validate_no_links(value):
    if re.search(r'\bhttps?://', value):
        raise ValidationError("Campul nu trebuie sa contina linkuri.")
    
def same_email(value1, value2):
    if value1 != value2:
        raise ValidationError("Adresele de email nu coincid.")
    


#Formular

class ContactForm(forms.Form):

    nume = forms.CharField(
        label="Nume",
        max_length=10,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Nume'}),
        validators=[validate_capital_after_space, validate_capital_clean]
    )
    prenume = forms.CharField(
        label="Prenume",
        max_length=10,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Prenume'}),
        validators=[validate_capital_after_space, validate_capital_clean]
    )
    cnp = forms.CharField(
        label="CNP",
        max_length=13,
        min_length=13,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': '13 cifre'}),
        validators=[validate_cnp]
    )
    data_nasterii = forms.DateField(
        label="Data nașterii",
        required=True,
        widget=forms.DateInput(attrs={'type': 'date'}),
        validators=[validate_major]
    )
    email = forms.EmailField(
        label="Email",
        required=True,
        validators =[validate_email_temp],
    )
    confirmare_email = forms.EmailField(
        label="Confirmare email",
        required=True,
        validators=[validate_email_temp],
    )
    
    TIP_MESAJ_CHOICES = [
        ('neselectat', 'Neselectat'),
        ('reclamatie', 'Reclamație'),
        ('intrebare', 'Întrebare'),
        ('review', 'Review'),
        ('cerere', 'Cerere'),
        ('programare', 'Programare'),
    ]



    tip_mesaj = forms.ChoiceField(
        label="Tip mesaj",
        choices=TIP_MESAJ_CHOICES,
        required=True,
        initial='neselectat'
    )

    subiect = forms.CharField(
        label="Subiect",
        max_length=100,
        required=True,
        validators = [validate_no_links, validate_capital_clean]
    )

    minim_zile_asteptare = forms.IntegerField(
        label="Minim zile asteptare",
        min_value=1,
        max_value=30,
        required=True,
        help_text=(
            "Pentru review-uri/cereri minimul este 4 zile, "
            "iar pentru întrebări de la 2 încolo. Maximul e 30."
        )
    )

    mesaj = forms.CharField(
        label="Mesaj (nu uita să te semnezi la final)",
        widget=forms.Textarea(attrs={'rows': 4, 'placeholder': 'Scrie mesajul tau aici și semneaza-te...'}),
        required=True,
        validators=[validate_no_links, validate_message]
    )





# Validari suplimentare

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        confirmare_email = cleaned_data.get('confirmare_email')
        nume = cleaned_data.get('nume')
        mesaj = cleaned_data.get('mesaj')
        tip_mesaj = cleaned_data.get('tip_mesaj')
        zile = cleaned_data.get('minim_zile_asteptare')
        cnp = cleaned_data.get('cnp')
        data_nasterii = cleaned_data.get('data_nasterii')

        if email and confirmare_email and email != confirmare_email:
            self.add_error('confirmare_email', "Adresele de email nu coincid.")

        if mesaj and nume:
            cuvinte = mesaj.strip().split()
            #semnat nume la final
            if not cuvinte or cuvinte[-1].lower() != nume.lower():
                self.add_error('mesaj', "Mesajul trebuie semnat cu numele tau la final.")

        if tip_mesaj and zile:
            if tip_mesaj in ['review', 'cerere'] and zile < 4:
                self.add_error('minim_zile_asteptare', "Pentru review-uri sau cereri trebuie minim 4 zile de asteptare.")
            elif tip_mesaj in ['reclamatie', 'intrebare'] and zile < 2:
                self.add_error('minim_zile_asteptare', "Pentru reclamatii sau intrebari trebuie minim 2 zile de asteptare.")
            elif zile > 30:
                self.add_error('minim_zile_asteptare', "Numarul maxim de zile de asteptare este 30.")

        if cnp and data_nasterii:
            try:
                an = int(cnp[1:3])
                luna = int(cnp[3:5])
                zi = int(cnp[5:7])
                if cnp[0] in ['1', '2']:
                    an += 1900
                elif cnp[0] in ['5', '6']:
                    an += 2000
                data_cnp = date(an, luna, zi)
                if data_cnp != data_nasterii:
                    self.add_error('cnp', "CNP-ul nu corespunde cu data nasterii.")
            except Exception:
                self.add_error('cnp', "CNP-ul contine o data invalida.")

    
    # Preprocesari date
    
        if data_nasterii:
            azi = date.today()
            ani = azi.year - data_nasterii.year
            luni = azi.month - data_nasterii.month
            if azi.day < data_nasterii.day:
                luni -= 1
            if luni < 0:
                ani -= 1
                luni += 12
            cleaned_data['varsta_formatata'] = f"{ani} ani și {luni} luni"

        if mesaj:
            mesaj_curat = " ".join(mesaj.split())
            rezultat = []
            urmeaza_majuscula = True

            for caracter in mesaj_curat:
                if urmeaza_majuscula and caracter.isalpha():
                    rezultat.append(caracter.upper())
                    urmeaza_majuscula = False
                else:
                    rezultat.append(caracter)

                if caracter in ".!?":
                    urmeaza_majuscula = True

            mesaj_curat = "".join(rezultat)

            cleaned_data['mesaj'] = mesaj_curat


        if tip_mesaj and zile:
            urgent = False
            if (tip_mesaj in ['review', 'cerere'] and zile == 4) or \
            (tip_mesaj in ['reclamatie', 'intrebare'] and zile == 2):
                urgent = True
            cleaned_data['urgent'] = urgent

        return cleaned_data


#Filtru produse

class FiltruProduseForm(forms.Form):
    nume = forms.CharField(required=False, label="Nume produs")
    pret_min = forms.DecimalField(required=False, min_value=0, label="Pret minim")
    pret_max = forms.DecimalField(required=False, min_value=0, label="Pret maxim")
    categorie = forms.ModelChoiceField(
        queryset=Categorie.objects.all(),
        required=False,
        label="Categorie",
        empty_label="Toate categoriile"
    )
    produse_pe_pagina = forms.IntegerField(required=False, min_value=1, max_value=12, initial=10, label="Produse/pagina")

    def clean(self):
        cleaned_data = super().clean()
        pret_min = cleaned_data.get("pret_min")
        pret_max = cleaned_data.get("pret_max")
        if pret_min and pret_max and pret_min > pret_max:
            raise ValidationError("Pretul minim nu poate fi mai mare decat pretul maxim.")
        return cleaned_data



###LOGIN
class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label="Username")
    password = forms.CharField(widget=forms.PasswordInput(), label="Parola")
    remember_me = forms.BooleanField(required=False, label="Tine minte timp de o zi")

#genereaza_cod
def genereaza_cod(lungime=20):
    caractere = string.ascii_letters + string.digits
    return ''.join(secrets.choice(caractere) for _ in range(lungime))

User = get_user_model()
###REGISTER
class UserRegisterForm(forms.ModelForm):
    password1 = forms.CharField(label="Parola", widget=forms.PasswordInput())
    password2 = forms.CharField(label="Confirmă parola", widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "nr_tel",
            "data_nasterii",
            "vip",
            "adresa",
            "tara",

        ]

        widgets = {
            "data_nasterii": forms.DateInput(attrs={"type": "date"}),
        }

    # VALIDARE TELEFON
    def clean_nr_tel(self):
        nr_tel = self.cleaned_data["nr_tel"]
        if not nr_tel.isdigit():
            raise ValidationError("Numarul de telefon trebuie sa contina doar cifre.")
        if len(nr_tel) < 10:
            raise ValidationError("Numarul de telefon trebuie să aibă cel puțin 10 caractere.")
        return nr_tel

    def clean_tara(self):
        tara = self.cleaned_data["tara"]
        if len(tara) < 3:
            raise ValidationError("Numele țării trebuie să aibă cel puțin 3 caractere.")
        return tara

    
    def clean_data_nasterii(self):
        data_n = self.cleaned_data["data_nasterii"]
        if data_n > date.today():
            raise ValidationError("Data nașterii nu poate fi în viitor.")
        return data_n

    # VALIDARE PAROLE
    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get("password1")
        p2 = cleaned_data.get("password2")

        if p1 and p2 and p1 != p2:
            raise ValidationError("Parolele nu coincid!")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)

        user.set_password(self.cleaned_data["password1"])
        user.cod = genereaza_cod(20)
        user.blocat = False

        if commit:
            user.save()

        return user


#validatori custom
def validare_numar_pozitiv(value):
    if value <= 0:
        raise ValidationError("Valoarea trebuie sa fie mai mare decat 0.")

def validare_maxim_100(value):
    if value > 100:
        raise ValidationError("Valoarea nu poate depasi 100.")



#Introd prod

class ProdusForm(forms.ModelForm):
    pret_cumparare = forms.DecimalField(
        max_digits=7, decimal_places=2, 
        label="Pret de cumparare",
        help_text="Introduceti pretul de cumparare de la furnizor",
        validators=[validare_numar_pozitiv]
    )
    marja_procent = forms.DecimalField(
        max_digits=5, decimal_places=2, 
        label="Marja (%)",
        help_text="Introduceti procentajul de adaos comercial",
        validators=[validare_numar_pozitiv, validare_maxim_100]
    )

    class Meta:
        model = Produs
        fields = ['name', 'stock_quantity', 'weight', 'is_active', 'categorie', 'furnizor']
        labels = {
            'name': 'Denumire Produs',
            'stock_quantity': 'Cantitate în stoc'
        }
        help_texts = {
            'weight': 'Introduceti greutatea produsului în kilograme.',
            'name' : 'Introduceti numele produsului'
        }

    def clean_weight(self):
        weight = self.cleaned_data.get('weight')
        if weight <= 0:
            raise ValidationError("Greutatea trebuie sa fie mai mare decat 0.")
        return weight

    # Validare cu 2 cmp
    def clean(self):
        cleaned_data = super().clean()
        pret_cumparare = cleaned_data.get('pret_cumparare')
        marja = cleaned_data.get('marja_procent')

        if pret_cumparare and marja:
            if pret_cumparare > 1000 and marja < 5:
                raise ValidationError("Pentru produse scumpe, marja trebuie sa fie cel putin 5%.")
        
        return cleaned_data

    # commit = false
    def save(self, commit=True):
        produs = super().save(commit=False)
        pret_cumparare = self.cleaned_data.get('pret_cumparare')
        marja = self.cleaned_data.get('marja_procent')

        
        if pret_cumparare and marja is not None:
            produs.price = pret_cumparare * (1 + marja / 100)

        if commit:
            produs.save()
        return produs



class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'nr_tel', 'adresa', 'tara', 'data_nasterii']
        labels = {
            'nr_tel': 'Număr Telefon',
            'adresa': 'Adresă Completă'
        }

