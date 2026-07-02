from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Conversation, Message
from .forms import MessageForm
from listings.models import Listing


@login_required
def inbox(request):
    conversations = Conversation.objects.filter(
        Q(buyer=request.user) | Q(seller=request.user)
    ).order_by('-updated_at')
    return render(request, 'messaging/inbox.html', {
        'conversations': conversations,
    })


@login_required
def conversation_detail(request, pk):
    conversation = get_object_or_404(
        Conversation.objects.filter(
            Q(buyer=request.user) | Q(seller=request.user)
        ),
        pk=pk
    )
    
    # Mark messages as read
    conversation.messages.filter(is_read=False).exclude(sender=request.user).update(is_read=True)
    
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.conversation = conversation
            message.sender = request.user
            message.save()
            conversation.save()  # Update updated_at
            return redirect('conversation_detail', pk=pk)
    else:
        form = MessageForm()
    
    return render(request, 'messaging/conversation_detail.html', {
        'conversation': conversation,
        'form': form,
    })


@login_required
def start_conversation(request, listing_pk):
    listing = get_object_or_404(Listing, pk=listing_pk)
    
    if listing.seller == request.user:
        messages.error(request, 'Vous ne pouvez pas vous contacter vous-même.')
        return redirect('listing_detail', pk=listing_pk)
    
    conversation, created = Conversation.objects.get_or_create(
        listing=listing,
        buyer=request.user,
        defaults={'seller': listing.seller}
    )
    
    return redirect('conversation_detail', pk=conversation.pk)
