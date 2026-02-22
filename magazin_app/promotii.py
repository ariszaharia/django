from django import forms
from .models import Categorie, PromotieNoua

class PromotieNouaForm(forms.ModelForm):
    subiect = forms.CharField(max_length=200)
    mesaj = forms.CharField(widget=forms.Textarea)
    
    categorii = forms.ModelMultipleChoiceField(
        queryset=Categorie.objects.filter(status="activ"),
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = PromotieNoua
        fields = ["nume", "data_expirare", "reducere", "descriere", "categorii"]