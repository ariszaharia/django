import datetime
from django.contrib import messages
from django.conf import settings
from .utils import Accesare

LOG_ACCESARI = []

class MiddlewareNou:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            user = request.user
            
            if not user.nr_tel or not user.adresa:
                acum = datetime.datetime.now().timestamp()
                
                ultima_notificare = request.session.get('ultima_notificare_timp', 0)
                interval_secunde = settings.NZL * 24 * 3600
                
                if acum - ultima_notificare >= interval_secunde:
                    
                    if not request.session.get('notificare_afisata_acum', False):
                        
                        lipsa = []
                        if not user.nr_tel: lipsa.append("Telefon")
                        if not user.adresa: lipsa.append("Adresă")
                        
                        mesaj_html = "Profil incomplet! Vă rugăm să completați: <ul>"
                        for camp in lipsa:
                            mesaj_html += f"<li>{camp}</li>"
                        mesaj_html += "</ul>"
                        
                        messages.warning(request, mesaj_html)
                        
                        request.session['notificare_afisata_acum'] = True
                        request.session['ultima_notificare_timp'] = acum
                else:
                    request.session['notificare_afisata_acum'] = False

        request.proprietate_noua = 17 
        response = self.get_response(request)      

        acc = Accesare(request)
        LOG_ACCESARI.append(acc)

        return response