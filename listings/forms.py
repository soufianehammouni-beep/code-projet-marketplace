from django import forms
from .models import Listing, ListingPhoto, Category


class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'description', 'price', 'category', 'city']
        labels = {
            'title': 'Titre',
            'description': 'Description',
            'price': 'Prix',
            'category': 'Catégorie',
            'city': 'Ville',
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
            'price': forms.NumberInput(attrs={'step': '0.01'}),
        }


class ListingFilterForm(forms.Form):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        label='Catégorie',
        empty_label='Toutes les catégories'
    )
    min_price = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=False,
        label='Prix minimum',
        widget=forms.NumberInput(attrs={'placeholder': 'Min'})
    )
    max_price = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=False,
        label='Prix maximum',
        widget=forms.NumberInput(attrs={'placeholder': 'Max'})
    )
    city = forms.CharField(
        max_length=100,
        required=False,
        label='Ville',
        widget=forms.TextInput(attrs={'placeholder': 'Ville'})
    )
    q = forms.CharField(
        max_length=200,
        required=False,
        label='Recherche',
        widget=forms.TextInput(attrs={'placeholder': 'Rechercher...'})
    )

