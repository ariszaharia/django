from datetime import datetime
import secrets
import string

def get_ip(request):
    str_lista_ip = request.META.get('HTTP_X_FORWARDED_FOR')
    if str_lista_ip:
        return str_lista_ip.split(',')[-1].strip()
    else:
        return request.META.get('REMOTE_ADDR')

def genereaza_cod(lungime=20):
    caractere = string.ascii_letters + string.digits  
    return ''.join(secrets.choice(caractere) for _ in range(lungime))


class Accesare:
    contor_id = 1  
    
    def __init__(self, request):
        self.id = Accesare.contor_id
        Accesare.contor_id += 1
        self.ip_client = get_ip(request)
        self.url = request.path
        self.data = datetime.now()

    def lista_parametri(self):
        return [
            ("id", self.id if self.id else None),
            ("ip_client", self.ip_client if self.ip_client else None),
            ("url", self.url if self.url else None),
            ("data", self.data if self.data else None),
        ]
        
    def get_url(self):
        return self.url
        
    def get_data_formatata(self, format_str="%d-%m-%Y %H:%M:%S"):
        return self.data.strftime(format_str) if self.data else None
        
    def pagina(self):
        if not self.url:
            return "/"
        path = self.url.split("?", 1)[0]
        return path if path else "/"  


