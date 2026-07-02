from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Avg
from .models import Review
from .forms import ReviewForm
from listings.models import Listing


@login_required
def create_review(request, listing_pk):
    listing = get_object_or_404(Listing, pk=listing_pk)
    
    # Check if user can review (not the seller, and listing is sold)
    if listing.seller == request.user:
        messages.error(request, 'Vous ne pouvez pas vous évaluer vous-même.')
        return redirect('listing_detail', pk=listing_pk)
    
    if listing.status != 'sold':
        messages.error(request, 'Vous ne pouvez évaluer que les annonces vendues.')
        return redirect('listing_detail', pk=listing_pk)
    
    # Check if already reviewed
    if Review.objects.filter(listing=listing, reviewer=request.user).exists():
        messages.error(request, 'Vous avez déjà laissé un avis pour cette annonce.')
        return redirect('listing_detail', pk=listing_pk)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.listing = listing
            review.reviewer = request.user
            review.reviewed_user = listing.seller
            review.save()
            messages.success(request, 'Avis publié avec succès !')
            return redirect('listing_detail', pk=listing_pk)
    else:
        form = ReviewForm()
    
    return render(request, 'reviews/create_review.html', {
        'form': form,
        'listing': listing,
    })


def user_reviews(request, username):
    from django.contrib.auth.models import User
    user = get_object_or_404(User, username=username)
    reviews = user.reviews_received.all().order_by('-created_at')
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg']
    return render(request, 'reviews/user_reviews.html', {
        'reviewed_user': user,
        'reviews': reviews,
        'avg_rating': avg_rating,
    })

