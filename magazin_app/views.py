from django.http import HttpResponseForbidden
from django.contrib.auth.models import Group
from datetime import datetime, timedelta
from django.shortcuts import render
from .middleware import LOG_ACCESARI
from .models import Produs, Categorie, User, Vizualizare, Comanda
from django.core.paginator import Paginator
from .forms import ContactForm, FiltruProduseForm, UserLoginForm, UserRegisterForm, ProdusForm, UpdateProfileForm
from .promotii import PromotieNouaForm
from django.shortcuts import redirect
import json
import os
import time
from django.contrib import messages
from django import forms
from collections import Counter
from django.core.mail import send_mail, mail_admins, send_mass_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.db.models import Count
from django.contrib.auth import authenticate, login, logout
from django.db.models import Case, When, Value, IntegerField
from django.http import JsonResponse
from django.core.mail import EmailMessage
from xhtml2pdf import pisa
from django.db import transaction
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from django.core.cache import cache



def index(request):
    categorii = Categorie.objects.all()
    return render(request, 'magazin_app/home.html', {
        "ip": get_ip(request),
        "categorii_meniu" : categorii
    })

def info(request):
    nr_403 = request.session.get("nr_403", 0) + 1
    request.session["nr_403"] = nr_403
    if "user_id" not in request.session:
        html = render_to_string("magazin_app/403.html", {
            "titlu": "Eroare vizualizare pagina",
            "mesaj_personalizat": "Trebuie să fii logat.",
        })
        return HttpResponseForbidden(html)

    user = User.objects.get(id=request.session["user_id"])

    grup = Group.objects.get(name="Administratori_site")

    if grup not in user.groups.all():
        html = render_to_string("magazin_app/403.html", {
            "titlu": "Eroare vizualizare pagina",
            "mesaj_personalizat": "Nu ai voie vizualizezi pagina.",
            "utilizator": user,
            "nr_403": nr_403,
            "limita": settings.N_MAX_403,
        })
        return HttpResponseForbidden(html)

    param_data = request.GET.get("data")
    html_content = afis_data(param_data)

    nr_parametri = len(request.GET)
    parametrii = request.GET.items()

    context = {
        "html_content": html_content,
        "nr_parametri" : nr_parametri,
        "parametrii" : parametrii,
        "ip": get_ip(request),
    }
    return render(request, "magazin_app/info.html", context)



def afis_data(param):
    now = datetime.now()
    
    luni = ["ianuarie", "februarie", "martie", "aprilie", "mai", "iunie",
            "iulie", "august", "septembrie", "octombrie", "noiembrie", "decembrie"]
    zile = ["luni", "marti", "miercuri", "joi", "vineri", "sambata", "duminica"]
    
    if param == "zi":
        data_afis = f"{zile[now.weekday()]}, {now.day} {luni[now.month - 1]} {now.year}"
        return f"<h2>Data:</h2><p>{data_afis}</p>"
    
    elif param == "timp":
        timp_afis = f"{now.hour:02d}:{now.minute:02d}:{now.second:02d}"
        return f"<h2>Ora:</h2><p>{timp_afis}</p>"
    
    elif param is None:
        data_timp_afis = f"{zile[now.weekday()]}, {now.day} {luni[now.month - 1]} {now.year} {now.hour:02d}:{now.minute:02d}:{now.second:02d}"
        return f"<h2>Data si ora:</h2><p>{data_timp_afis}</p>"
    


def afis_template(request):
    return render(request,"magazin_app/exemplu.html",
        {
            "titlu_tab":"Titlu fereastra",
            "titlu_articol":"Titlu afisat",
            "continut_articol":"Continut text"
        }
    )


def get_ip(request):
    req_headers = request.META
    str_lista_ip = request.META.get('HTTP_X_FORWARDED_FOR')
    if str_lista_ip:
        return str_lista_ip.split(',')[-1].strip()
    else:
        return request.META.get('REMOTE_ADDR')



def log(request):
    nr_403 = request.session.get("nr_403", 0) + 1
    request.session["nr_403"] = nr_403
    if "user_id" not in request.session:
        html = render_to_string("magazin_app/403.html", {
            "titlu": "Eroare vizualizare log",
            "mesaj_personalizat": "Trebuie să fii logat.",
        })
        return HttpResponseForbidden(html)

    user = User.objects.get(id=request.session["user_id"])
    grup = Group.objects.get(name="Administratori_site")

    if grup not in user.groups.all():
        html = render_to_string("magazin_app/403.html",{
            "titlu": "Eroare vizualizare log",
            "mesaj_personalizat": "Nu ai voie vizualizezi log-ul.",
            "utilizator": user,
            "nr_403": nr_403,
            "limita": settings.N_MAX_403,
        })
        return HttpResponseForbidden(html)


    param_ultimele = request.GET.get("ultimele")
    param_accesari = request.GET.get("accesari")
    param_iduri = request.GET.getlist("iduri")
    param_dubluri = request.GET.get("dubluri", "false").lower() == "true"
    param_tabel = request.GET.get("tabel")

    mesaje = []
    tabel = []
    coloane = []
    rezumat = {}

    if param_ultimele is not None:
        if not param_ultimele.isnumeric():
            mesaje.append("Eroare: parametrul 'ultimele' trebuie să fie un număr.")
        else:
            n = int(param_ultimele)
            k = len(LOG_ACCESARI)
            ultimele = LOG_ACCESARI[-n:] if n <= k else LOG_ACCESARI
            mesaje.extend([
                f"[{acc.id}] - {acc.get_data_formatata()} — {acc.pagina()} — {acc.ip_client}"
                for acc in ultimele
            ])
            if n > k:
                mesaje.append(f"<span style='color:red;'>Exista doar {k} accesari fata de {n} cerute.</span>")

    elif param_tabel:
        if param_tabel.lower() == "tot":
            coloane = ["id", "url", "ip_client", "data"]
        else:
            coloane = [c.strip() for c in param_tabel.split(",")]
        for acc in LOG_ACCESARI:
            rand = [getattr(acc, col, "") for col in coloane]
            tabel.append(rand)

    elif not param_ultimele and not param_tabel:
        mesaje.extend([
            f"[{acc.id}] - {acc.pagina()} - {acc.ip_client}"
            for acc in LOG_ACCESARI
        ])

    if param_accesari is not None:
        if param_accesari == "detalii":
            mesaje.extend([
                f"[{acc.id}] - {acc.pagina()} - {acc.get_data_formatata()}"
                for acc in LOG_ACCESARI
            ])
        elif param_accesari.isnumeric():
            n = int(param_accesari)
            total = len(LOG_ACCESARI)
            if n <= total:
                mesaje.append(f"<span style='color:green;'>Număr total de accesări: {total}</span>")
            else:
                mesaje.append(f"<span style='color:red;'>Exista doar {total} accesari fata de {n} cerute.</span>")

    elif param_iduri:
        iduri = []
        iduri_gasite = []
        for grup in param_iduri:
            for val in grup.split(","):
                try:
                    iduri.append(int(val))
                except:
                    pass
        if param_dubluri is False:
            for id in iduri:
                for acc in LOG_ACCESARI:
                    if acc.id == id and id not in iduri_gasite:
                        iduri_gasite.append(id)
                        mesaje.append(f"[{acc.id}] - {acc.get_data_formatata()} — {acc.pagina()} — {acc.ip_client}")
                        break
        else:
            for id in iduri:
                for acc in LOG_ACCESARI:
                    if acc.id == id:
                        mesaje.append(f"[{acc.id}] - {acc.get_data_formatata()} — {acc.pagina()} — {acc.ip_client}")

    if LOG_ACCESARI:
        numarari = Counter([acc.pagina() for acc in LOG_ACCESARI])
        cea_mai_frecventa, nr_max = numarari.most_common(1)[0]
        cea_mai_putin_frecventa, nr_min = numarari.most_common()[-1]
        rezumat = {
            "cea_mai_frecventa": cea_mai_frecventa,
            "nr_max": nr_max,
            "cea_mai_putin_frecventa": cea_mai_putin_frecventa,
            "nr_min": nr_min,
        }

    context = {
        "mesaje": mesaje,
        "tabel": tabel,
        "coloane": coloane,
        "rezumat": rezumat,
        "ip": get_ip(request),
    }

    return render(request, "magazin_app/log.html", context)


def despre(request):
    categorii = Categorie.objects.all()
    return render(request, "magazin_app/despre.html", {
        "ip": get_ip(request),
        "categorii_meniu" : categorii
    })



def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():  
            data = form.cleaned_data
            data.pop('confirmare_email', None)
            urgent = data.get('urgent', False)
            timestamp = int(time.time())

            nume_fisier = f"mesaj_{timestamp}{'_urgent' if urgent else ''}.json"
            folder_path = os.path.join(os.path.dirname(__file__), 'Mesaje')

            date_utilizator = {
                "ip_client": get_ip(request),
                "data_trimiterii": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }

            continut_fisier = {
                "date_utilizator" : date_utilizator,
                "formular" : data
            }
            cale_completa = os.path.join(folder_path, nume_fisier)
            with open(cale_completa, 'w') as f:
                json.dump(continut_fisier, f, ensure_ascii=False, indent=4, default=str)

            return redirect('mesaj_trimis')
    else:
        form = ContactForm()
    
    categorii = Categorie.objects.all()
    return render(request, 'magazin_app/contact.html', 
        {
        "ip": get_ip(request),
        'form': form,
        "categorii_meniu" : categorii
        }
    )



def cos(request):
    categorii = Categorie.objects.all()
    return render(request, "magazin_app/cos.html",{
        "ip": get_ip(request),
        "categorii_meniu" : categorii
    })

def produse(request):
    sortare = request.GET.get("sort", "none")
    user_id = request.user.id if request.user.is_authenticated else "anonim"
    cache_key = f"produse_pagina_{user_id}" 

    produse = Produs.objects.annotate(
        available = Case(
            When(stock_quantity__gt=0, then=Value(1)),
            default=Value(0),
            output_field=IntegerField()
        )
    )

    form = FiltruProduseForm(request.GET or None)
    categorii = Categorie.objects.all()
    if form.is_valid():
        nume = form.cleaned_data.get("nume")
        pret_min = form.cleaned_data.get("pret_min")
        pret_max = form.cleaned_data.get("pret_max")
        categorie = form.cleaned_data.get("categorie")
        data_adaugare = form.cleaned_data.get("data_adaugare")
        produse_pe_pagina = form.cleaned_data.get("produse_pe_pagina") or 10
        cache.set(cache_key, produse_pe_pagina, 86400)

        if nume:
            produse = produse.filter(name=nume)
        if pret_min is not None:
            produse = produse.filter(price__gte=pret_min)
        if pret_max is not None:
            produse = produse.filter(price__lte=pret_max)
        if categorie:
            produse = produse.filter(categorie=categorie)
        if data_adaugare:
            produse = produse.filter(data_adaugare__date=data_adaugare)
    else:
        produse_pe_pagina = cache.get(cache_key, 10)

    if sortare == "a":
        produse = produse.order_by("-price", "price")
    elif sortare == "d":
        produse = produse.order_by("-available", "-price")
    else:
        produse = produse.order_by("-available", "name")

    paginator = Paginator(produse, produse_pe_pagina)
    page_number = request.GET.get("page", 1)

    try:
        page_num = int(page_number)
    except ValueError:
        page_num = 1

    if "salt" in request.GET:
        if page_num > paginator.num_pages:
            page_num = paginator.num_pages
            messages.warning(request, "Nu mai sunt prajituri.")

    page_obj = paginator.get_page(page_num)

    salt_3 = page_obj.number + 3



    if not produse.exists():
        messages.warning(request, "Nu s-au gasit produse care corespund filtrului.")
    if "produse_pe_pagina" in request.GET:
        messages.info(request, "Dupa repaginare, unele produse pot fi omise sau repetate.")

    return render(request, "magazin_app/produse.html", {
        "page_obj": page_obj,
        "form": form,
        "sortare": sortare,
        "ip": get_ip(request),
        "categorii_meniu" : categorii,
        "salt_3" : salt_3
    })


def afis_produse(request, produs_id):
    produs = Produs.objects.filter(produs_id=produs_id).first()

    if not produs:
        return render(request, "magazin_app/eroare404.html", {
            "mesaj": "Produsul căutat nu există.",
            "ip": get_ip(request),
        })
    
    if request.session.get("user_id"):
        user = User.objects.get(id=request.session["user_id"])

        Vizualizare.objects.create(user=user, produs=produs)

        N = 5
        toate_viz = Vizualizare.objects.filter(user=user).order_by('-data_vizualizare')

        if toate_viz.count() > N:
            for viz in toate_viz[N:]:
                viz.delete()

    return render(request, "magazin_app/produs_detalii.html", {
        "produs": produs,
        "ip": get_ip(request),
    })



def categorie_detalii(request, nume_categorie):
    try:
        categorie = Categorie.objects.get(name__iexact=nume_categorie)
    except Categorie.DoesNotExist:
        return render(request, "magazin_app/eroare404.html", {
            "mesaj": f"Categoria '{nume_categorie}' nu exista.",
            "ip": get_ip(request),
        })

    produse_categorie = Produs.objects.filter(categorie=categorie)
    form = FiltruProduseForm(request.GET or None, initial={"categorie": categorie.categorie_id})

    form.fields["categorie"].initial = categorie.categorie_id
    form.fields["categorie"].widget.attrs.update({
        "readonly": True,
        "hidden": True,
    })

    categorie_input = request.GET.get("categorie")
    if categorie_input and str(categorie_input) != str(categorie.categorie_id):
        return render(request, "magazin_app/eroare.html", {
            "mesaj": "Eroare: Valoarea categoriei a fost modificata",
            "ip": get_ip(request),
        })

    if form.is_valid():
        filtre = form.cleaned_data

        if filtre.get("nume"):
            produse_categorie = produse_categorie.filter(name__icontains=filtre["nume"])

        if filtre.get("pret_min") is not None:
            produse_categorie = produse_categorie.filter(price__gte=filtre["pret_min"])

        if filtre.get("pret_max") is not None:
            produse_categorie = produse_categorie.filter(price__lte=filtre["pret_max"])

        if filtre.get("data_adaugare"):
            produse_categorie = produse_categorie.filter(data_adaugare__date=filtre["data_adaugare"])

    sortare = request.GET.get("sort", "none")
    if sortare == "a":
        produse_categorie = produse_categorie.order_by("price")
    elif sortare == "d":
        produse_categorie = produse_categorie.order_by("-price")

    produse_pe_pagina = form.cleaned_data.get("produse_pe_pagina", 5) if form.is_valid() else 10
    paginator = Paginator(produse_categorie, produse_pe_pagina)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    categorii = Categorie.objects.all()


    return render(request, "magazin_app/produse.html", {
        "page_obj": page_obj,
        "form": form,
        "categorie": categorie,
        "sortare": sortare,
        "ip": get_ip(request),
        "categorii_meniu": categorii
    })
    
def categorie(request):
    return render(request, "magazin_app/categorii.html",{
        "ip" : get_ip(request) 
    })



def register_view(request):
    if request.method == 'POST':

        if request.POST.get("username", "").lower() == "admin":
            mail_admins(
                subject="cineva incearca sa ne preia site-ul",
                message=f"Email încercare: {request.POST.get('email')}",
                html_message=f"""
                    <h1 style='color:red'>Cineva incearca sa ne preia site-ul</h1>
                    <p>Email folosit: <b>{request.POST.get('email')}</b></p>
                """
            )
            messages.error(request, "Nu poti folosi acest username.")
            return redirect("register")
        

        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()

            link_confirmare = f"http://127.0.0.1:8000/confirma_mail/{user.cod}/"

            mesaj_html = render_to_string("magazin_app/confirmare_mail.html", {
                "user": user,
                "link_confirmare": link_confirmare
            })

            send_mail(
                subject="Confirma adresa ta de email",
                message="",
                html_message=mesaj_html,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
            )


            return render(request, "magazin_app/verifica_mail.html", {
                "email": user.email
            })

    else:
        form = UserRegisterForm()

    return render(request, 'magazin_app/register.html', {
        'form': form,
        "ip": get_ip(request)
    })

def confirma_mail(request, cod):
    try:
        user = User.objects.get(cod=cod)
        user.email_confirmat = True
        user.cod = None
        user.save()

        return render(request, "magazin_app/mail_confirmat.html", {
            "user": user
        })

    except User.DoesNotExist:
        messages.error(request, "Cod invalid sau expirat.")
        return redirect('index')




def login_view(request):
    if request.session.get('user_id'):
        return redirect('profile')

    if request.method == 'POST':
        form = UserLoginForm(data=request.POST, request=request)
        
        if form.is_valid():
            user = form.get_user()
            
            if not user.email_confirmat:
                messages.error(request, "Trebuie sa iti confirmi emailul inainte de a te loga.")
                return redirect('login')
            
            if user.blocat:
                messages.warning(request, "Contul tau a fost blocat de un moderator.")
                return redirect('login')

            login(request, user)


            request.session['user_id'] = user.id
            request.session['username'] = user.username
            request.session['email'] = user.email
            request.session['tara'] = user.tara
            request.session['adresa'] = user.adresa
            request.session['vip'] = user.vip
            request.session['logged_in_at'] = str(datetime.now())
            request.session['is_admin_site'] = user.groups.filter(name='Administratori_site').exists() 
            request.session['is_admin_produse'] = user.groups.filter(name='Administratori_produse').exists()
            
            request.session["vizualizeaza_oferta"] = False
            request.session['failed_attempts'] = []

            remember_me = form.cleaned_data.get('remember_me')
            if remember_me:
                request.session.set_expiry(86400)
            else:
                request.session.set_expiry(0)

            return redirect('profile')

        else:
            username = request.POST.get('username', 'Necunoscut')
            
            incercari = request.session.get('failed_attempts', [])
            acum = datetime.now()
            
            incercari = [
                t for t in incercari if datetime.fromisoformat(t) > acum - timedelta(minutes=2)
            ]
            
            incercari.append(acum.isoformat())
            request.session["failed_attempts"] = incercari
            request.session.modified = True
            
            if len(incercari) >= 3:
                ip = get_ip(request)
                mail_admins(
                    subject="Logari suspecte",
                    message=f"Username: {username}\nIP: {ip}",
                    html_message=f"""
                        <h1 style='color:red'>Logari suspecte</h1>
                        <p><strong>Username:</strong> {username}</p>
                        <p><strong>IP:</strong> {ip}</p>
                    """
                )

            messages.error(request, "Date de login incorecte.")
            return redirect('login')

    else:
        form = UserLoginForm()

    return render(request, 'magazin_app/login.html', {
        'form': form,
        'ip': get_ip(request)
    })


def logout_view(request):
    request.session.flush()
    messages.info(request, "Te-ai delogat cu succes.")
    return redirect('login')

@cache_page(4320000)
@vary_on_cookie
def profile_view(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    
    user = {
    "user_id": request.session.get('user_id'),
    "username": request.session.get('username'),
    "email": request.session.get('email'),
    "tara": request.session.get('tara'),
    "adresa": request.session.get('adresa'),
    "vip": request.session.get('vip'),
    "logged_in_at": request.session.get('logged_in_at')
    }

    return render(request, 'magazin_app/profile.html', {
        "user" : user,
        "ip" : get_ip(request)
    })


def change_password_view(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    user = User.objects.get(pk=user_id)

    if request.method == 'POST':
        old_pass = request.POST.get('old_pass')
        new_pass = request.POST.get('new_pass')
        confirm = request.POST.get('confirm')

        if user.parola != old_pass:
            messages.error(request, "Parola veche nu este corecta.")
        elif new_pass != confirm:
            messages.error(request, "Parolele noi nu coincid.")
        else:
            user.parola = new_pass
            user.save()
            messages.success(request, "Parola a fost schimbata cu succes!")
            return redirect('profile')

    return render(request, 'magazin_app/change_password.html',{
        "ip" : get_ip(request)
    })


def adauga_produs(request):
    nr_403 = request.session.get("nr_403", 0) + 1
    request.session["nr_403"] = nr_403
    if "user_id" not in request.session:
        html = render_to_string("magazin_app/403.html", {
            "titlu": "Eroare adăugare produse",
            "mesaj_personalizat": "Trebuie să fii logat.",
        })
        return HttpResponseForbidden(html)

    user = User.objects.get(id=request.session["user_id"])

    try:
        grupa_prod = Group.objects.get(name="Administratori_produse")
    except Group.DoesNotExist:
        html = render_to_string("magazin_app/403.html", {
            "titlu": "Eroare adăugare produse",
            "mesaj_personalizat": "Grupul Administratori_produse nu exista.",
        })
        return HttpResponseForbidden(html)

    if grupa_prod not in user.groups.all():
        messages.debug(request, f"Utilizatorul {user.username} a incercat adaugarea de produse fara permisiune.")
        html = render_to_string("magazin_app/403.html", {
            "titlu": "Eroare adaugare produse",
            "mesaj_personalizat": "Nu ai voie să adaugi produse.",
            "utilizator": user,
            "nr_403": nr_403,
            "limita": settings.N_MAX_403,
        })
        return HttpResponseForbidden(html)
    

    if request.method == "POST":
        form = ProdusForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Produsul a fost adaugat cu succes!")
            return redirect('produse')
    else:
        form = ProdusForm()

    return render(request, 'magazin_app/adauga_produs.html', {
        'form': form,
        'ip' : get_ip(request)
        })


def promotii_view(request):
    if request.method == "POST":
        form = PromotieNouaForm(request.POST)

        if form.is_valid():
            try:
                promotie = form.save(commit=False)
                promotie.save()
                form.save_m2m()

            except Exception as e:
                mail_admins(
                    subject="Eroare la salvarea promotiei",
                    message=str(e),
                    html_message=f"""
                        <h1 style='color:red'>Eroare la salvarea promotiei</h1>
                        <div style='background:red;color:white;padding:10px'>
                            {str(e)}
                        </div>
                    """
                )
                messages.error(request, "A aparut o eroare! Administratorii au fost notificati.")
                return redirect("promotii")

            subiect = form.cleaned_data['subiect']
            mesaj = form.cleaned_data['mesaj']
            categorii_selectate = form.cleaned_data['categorii']

            data_expirare = promotie.data_expirare
            reducere = promotie.reducere
            descriere = promotie.descriere

            trimiteri = []

            K = 2

            for categorie in categorii_selectate:

                template_path = f"magazin_app/emails/{categorie.name.lower()}.txt"
                users = User.objects.filter(
                    id__in=Vizualizare.objects.filter(
                        produs__categorie=categorie
                    )
                    .values('user')
                    .annotate(cnt=Count('user'))
                    .filter(cnt__gte=K)
                    .values('user')
                )

                for user_obj in users:
                    text = render_to_string(template_path, {
                        "user": user_obj,
                        "subiect": subiect,
                        "data_expirare": data_expirare,
                        "reducere": reducere,
                        "descriere": descriere,
                        "mesaj": mesaj,
                    })

                    trimiteri.append((
                        subiect,
                        text,
                        settings.DEFAULT_FROM_EMAIL,
                        [user_obj.email],
                    ))

            send_mass_mail(trimiteri, fail_silently=False)

            messages.success(request, "Promotiile au fost trimise!")
            return redirect('promotii')

    else:
        form = PromotieNouaForm()

    return render(request, "magazin_app/promotii.html", {"form": form})


def pagina_interzisa(request, reason=""):
    nr_403 = request.session.get("nr_403", 0) + 1
    request.session["nr_403"] = nr_403

    context = {
        "titlu": "",
        "mesaj_personalizat": "Nu ai permisiunea sa accesezi aceasta resursa.",
        "nr_403": nr_403,
        "limita": settings.N_MAX_403,
    }

    return render(request, "magazin_app/403.html", context, status=403)

def activeaza_oferta(request):
    if not request.session.get("user_id"):
        return redirect("login")

    request.session["vizualizeaza_oferta"] = True

    return redirect("oferta")

def oferta(request):
    if not request.session.get("user_id"):
        return redirect("login")

    if not request.session.get("vizualizeaza_oferta"):
        nr_403 = request.session.get("nr_403", 0) + 1
        request.session["nr_403"] = nr_403

        html = render_to_string("magazin_app/403.html", {
            "titlu": "Eroare afisare oferta",
            "mesaj_personalizat": "Nu ai voie să vizualizezi oferta",
            "utilizator": request.session.get("username"), 
            "nr_403": nr_403,
            "limita": getattr(settings, "N_MAX_403", 5),
        }, request=request)

        return HttpResponseForbidden(html)

    return render(request, "magazin_app/oferta.html", {
        "ip": get_ip(request)
    })


def finalizeaza_comanda(request):
    if request.method != "POST":
        return JsonResponse({"success": False, "error": "Metoda nepermisa."})

    user_id = request.session.get('user_id')
    if not user_id:
        return JsonResponse({"success": False, "error": "Utilizator neautentificat."})

    try:
        user = User.objects.get(id=user_id)
        date_comanda = json.loads(request.body)
        produse_factura = []
        comanda = None

        with transaction.atomic():
            total_valoare = sum(float(v['price']) * int(v['qty']) for v in date_comanda.values())
            
            comanda = Comanda.objects.create(
                user=user,
                valoare=total_valoare,
                tip_ambalaj="cutie",
                curier="DHL",
            )

            for p_id, detalii in date_comanda.items():
                produs = Produs.objects.select_for_update().get(produs_id=p_id)
                cantitate = int(detalii['qty'])
                
                if produs.stock_quantity >= cantitate:
                    produs.stock_quantity -= cantitate
                    produs.save()
                else:
                    raise ValueError(f"Stoc insuficient pentru {produs.name}")

                comanda.produse.add(produs)
                produse_factura.append({
                    "name": produs.name,
                    "price": detalii['price'],
                    "qty": cantitate,
                    "total": float(detalii['price']) * cantitate,
                })

        timestamp = int(time.time())
        folder = os.path.join(settings.BASE_DIR, 'facturi', user.username)
        os.makedirs(folder, exist_ok=True)
        cale = os.path.join(folder, f"factura-{timestamp}.pdf")

        context = {
            'comanda': comanda,
            'produse': produse_factura,
            'user': user,
            'data_ora': time.strftime("%Y-%m-%d %H:%M:%S"),
            'admin_email': settings.DEFAULT_FROM_EMAIL,
        }
        
        html_factura = render_to_string('magazin_app/factura_pdf.html', context)
        
        with open(cale, 'wb') as f:
            pisa.CreatePDF(html_factura, dest=f)


        email = EmailMessage(
            subject=f"Factura comanda #{comanda.comanda_id}",
            body=f"Buna ziua, {user.first_name}! Va multumim pentru comanda.",
            to=[user.email],
            )
        email.attach_file(cale)
        email.send()
        
        return JsonResponse({"success": True, "message": "Comanda finalizata cu succes."})

    except User.DoesNotExist:
        return JsonResponse({"success": False, "error": "Utilizator inexistent."})
    except ValueError as e:
        return JsonResponse({"success": False, "error": str(e)})
    except Exception as e:
        print(f"EROARE: {e}") 
        return JsonResponse({"success": False, "error": "Eroare interna server."})
             
def actualizeaza_date(request):
    user = User.objects.get(id=request.session.get('user_id'))
    if request.method == "POST":
        form = UpdateProfileForm(request.POST, instance=user)
        
        if form.is_valid():
            if not form.has_changed():
                messages.info(request, "Nu ai realizat nicio modificare.")
                return redirect('profile')
            
            form.save()
            cache.clear()
            messages.success(request, "Datele au fost actualizate cu succes!")
            return redirect('profile')
    else:
        form = UpdateProfileForm(instance=user)
        
        campuri_optionale = {
            'tara': 'Țară',
            'data_nasterii': 'Data Nașterii',
            'vip' : 'Statut VIP'
        }
        lipsa = [nume for camp, nume in campuri_optionale.items() if not getattr(user, camp)]
        
        if lipsa:
            lista_html = "Următoarele câmpuri sunt necompletate: <ul>"
            for item in lipsa:
                lista_html += f"<li>{item}</li>"
            lista_html += "</ul>"
            messages.error(request, lista_html, extra_tags='danger')

    return render(request, 'magazin_app/actualizeaza_date.html', {'form': form})