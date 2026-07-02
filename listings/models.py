from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Nom')
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True, verbose_name='Description')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Catégorie'
        verbose_name_plural = 'Catégories'
        ordering = ['name']


class Listing(models.Model):
    STATUS_CHOICES = [
        ('active', 'Disponible'),
        ('sold', 'Vendu'),
        ('reserved', 'Réservé'),
    ]

    title = models.CharField(max_length=200, verbose_name='Titre')
    description = models.TextField(verbose_name='Description')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Prix')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='listings', verbose_name='Catégorie')
    city = models.CharField(max_length=100, verbose_name='Ville')
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listings', verbose_name='Vendeur')
    buyer = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='purchases', verbose_name='Acheteur')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active', verbose_name='Statut')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('listing_detail', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Annonce'
        verbose_name_plural = 'Annonces'
        ordering = ['-created_at']


class ListingPhoto(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='photos', verbose_name='Annonce')
    image = models.ImageField(upload_to='listing_photos/', verbose_name='Image')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Photo de {self.listing.title}"

    class Meta:
        verbose_name = 'Photo d\'annonce'
        verbose_name_plural = 'Photos d\'annonces'

