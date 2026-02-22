from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Produs,Locatie,Organizator, Categorie,Inventar,Promotie,Ingredient, Furnizor, User, Comanda, PuncteFidelitate, Review


admin.site.site_header = "Magazin Fitness - Panou de administrare"
admin.site.site_title = "Magazin Fitness Admin"
admin.site.index_title = "Administrare continut magazin"

class LocatieAdmin(admin.ModelAdmin):
    list_display = ('oras', 'judet') 
    list_filter = ('oras', 'judet')
    search_fields = ('oras',)  
    fieldsets = (
        ('Date generale', {
            'fields': ('oras', 'judet')
        }),
        ('Date Specificate', {
            'fields': ('adresa','cod_postal'),
            'classes': ('collapse',), 
        }),
    )

class ProdusAdmin(admin.ModelAdmin):
    list_display = ('price', 'name', 'weight', 'stock_quantity', 'furnizor', 'categorie', 'is_active')
    search_fields = ('name', 'furnizor__name')
    ordering = ('-price',)
    list_filter = ('categorie', 'furnizor', 'is_active')
    list_per_page = 5
    fieldsets = (
        ('Informații generale', {
            'fields': ('name', 'price', 'categorie', 'furnizor', 'is_active')
        }),
        ('Detalii suplimentare', {
            'fields': ('stock_quantity', 'weight'),
            'classes': ('collapse',),  
        }),
    )

class FurnizorAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'is_active')
    search_fields = ('name', 'email')

class CategorieAdmin(admin.ModelAdmin):
    search_fields = ('name',)

class InventarAdmin(admin.ModelAdmin):
    list_display = ('produs', 'locatie', 'cantitate')
    search_fields = ('produs__name', 'locatie__oras')

class PromotieAdmin(admin.ModelAdmin):
    list_display = ('titlu', 'discount_percentage', 'data_inceput', 'data_sfarsit', 'is_active')
    search_fields = ('titlu',)

class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'benefit', 'protein_per_100g', 'country_from')
    search_fields = ('name', 'country_from')




class ComandaAdmin(admin.ModelAdmin):
    list_display = ("comanda_id", "user", "valoare", "tip_ambalaj", "curier")
    list_filter = ("tip_ambalaj", "curier")
    search_fields = ("user__username",)

class PuncteFidelitateAdmin(admin.ModelAdmin):
    list_display = ("id_puncte", "user", "puncte_castigate", "multiplicator", "data_comenzii", "data_revendicarii")


class ReviewAdmin(admin.ModelAdmin):
    list_display = ("review_id", "user", "produs", "tip")
    search_fields = ("user__username", "produs__name")



from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Info Suplimentar', {'fields': ('nr_tel', 'adresa', 'tara', 'blocat', 'vip', 'data_nasterii')}),
    )

    def get_readonly_fields(self, request, obj=None):
        if request.user.groups.filter(name='Moderatori').exists() and not request.user.is_superuser:
            all_fields = []
            for fieldset in self.get_fieldsets(request, obj):
                for field in fieldset[1]['fields']:
                    all_fields.append(field)
            
            editable_fields = ['first_name', 'last_name', 'email', 'blocat']
            
            return [f for f in all_fields if f not in editable_fields]
            
        return super().get_readonly_fields(request, obj)

    def has_change_permission(self, request, obj=None):
        if request.user.groups.filter(name='Moderatori').exists():
            return True
        return super().has_change_permission(request, obj)

admin.site.register(User, CustomUserAdmin)



