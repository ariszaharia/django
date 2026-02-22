@ECHO OFF

IF EXIST backup.sql DEL backup.sql

ECHO Realizam procesarea tabelelor din schema 'django' (Docker)

(FOR %%t IN (
    "magazin_app_furnizor"
    "magazin_app_categorie"
    "magazin_app_produs"
    "magazin_app_inventar"
    "magazin_app_promotie"
    "magazin_app_ingredient"
    "magazin_app_organizator"
    "magazin_app_locatie"
) DO (
    ECHO Exportam Tabelul %%t
    
    docker exec django_db pg_dump --column-inserts --data-only --inserts -U aris -d fitness -t "django.%%~t" >> backup.sql
))

ECHO Backup finalizat! Verifica daca backup.sql are date.
PAUSE