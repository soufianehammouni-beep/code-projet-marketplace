from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Listing, ListingPhoto, Category
from .forms import ListingForm, ListingFilterForm


def home(request):
    listings = Listing.objects.filter(status='active').order_by('-created_at')[:8]
    categories = Category.objects.all()
    return render(request, 'listings/home.html', {
        'listings': listings,
        'categories': categories,
    })


def listing_list(request):
    listings = Listing.objects.filter(status='active').order_by('-created_at')
    form = ListingFilterForm(request.GET)
    
    if form.is_valid():
        data = form.cleaned_data
        if data.get('category'):
            listings = listings.filter(category=data['category'])
        if data.get('min_price'):
            listings = listings.filter(price__gte=data['min_price'])
        if data.get('max_price'):
            listings = listings.filter(price__lte=data['max_price'])
        if data.get('city'):
            listings = listings.filter(city__icontains=data['city'])
        if data.get('q'):
            q = data['q']
            listings = listings.filter(
                Q(title__icontains=q) | Q(description__icontains=q)
            )
    
    paginator = Paginator(listings, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'listings/listing_list.html', {
        'page_obj': page_obj,
        'form': form,
    })


def listing_detail(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    related_listings = Listing.objects.filter(
        category=listing.category, status='active'
    ).exclude(pk=pk)[:4]
    return render(request, 'listings/listing_detail.html', {
        'listing': listing,
        'related_listings': related_listings,
    })


@login_required
def listing_create(request):
    if request.method == 'POST':
        form = ListingForm(request.POST)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.seller = request.user
            listing.save()
            
            # Handle multiple photos
            photos = request.FILES.getlist('photos')
            for photo in photos:
                ListingPhoto.objects.create(listing=listing, image=photo)
            
            messages.success(request, 'Annonce publiée avec succès !')
            return redirect('listing_detail', pk=listing.pk)
    else:
        form = ListingForm()
    return render(request, 'listings/listing_form.html', {
        'form': form,
        'title': 'Nouvelle annonce',
    })


@login_required
def listing_update(request, pk):
    listing = get_object_or_404(Listing, pk=pk, seller=request.user)
    if request.method == 'POST':
        form = ListingForm(request.POST, instance=listing)
        if form.is_valid():
            form.save()
            
            photos = request.FILES.getlist('photos')
            for photo in photos:
                ListingPhoto.objects.create(listing=listing, image=photo)
            
            messages.success(request, 'Annonce mise à jour avec succès !')
            return redirect('listing_detail', pk=listing.pk)
    else:
        form = ListingForm(instance=listing)
    return render(request, 'listings/listing_form.html', {
        'form': form,
        'listing': listing,
        'title': 'Modifier l\'annonce',
    })


@login_required
def listing_delete(request, pk):
    listing = get_object_or_404(Listing, pk=pk, seller=request.user)
    if request.method == 'POST':
        listing.delete()
        messages.success(request, 'Annonce supprimée avec succès.')
        return redirect('listing_list')
    return render(request, 'listings/listing_confirm_delete.html', {
        'listing': listing,
    })


@login_required
def mark_sold(request, pk):
    listing = get_object_or_404(Listing, pk=pk, seller=request.user)
    from messaging.models import Conversation
    
    if request.method == 'POST':
        buyer_id = request.POST.get('buyer')
        if buyer_id:
            try:
                buyer = Conversation.objects.get(pk=buyer_id, listing=listing).buyer
                listing.buyer = buyer
            except Conversation.DoesNotExist:
                pass
        listing.status = 'sold'
        listing.save()
        messages.success(request, 'Annonce marquée comme vendue.')
        return redirect('listing_detail', pk=listing.pk)
    
    conversations = listing.conversations.select_related('buyer').all()
    return render(request, 'listings/mark_sold.html', {
        'listing': listing,
        'conversations': conversations,
    })


@login_required
def delete_photo(request, photo_pk):
    photo = get_object_or_404(ListingPhoto, pk=photo_pk, listing__seller=request.user)
    photo.delete()
    messages.success(request, 'Photo supprimée.')
    return redirect('listing_update', pk=photo.listing.pk)
