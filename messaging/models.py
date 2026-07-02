from django.db import models
from django.contrib.auth.models import User
from listings.models import Listing


class Conversation(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='conversations', verbose_name='Annonce')
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='conversations_as_buyer', verbose_name='Acheteur')
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='conversations_as_seller', verbose_name='Vendeur')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Conversation sur {self.listing.title}"

    class Meta:
        verbose_name = 'Conversation'
        verbose_name_plural = 'Conversations'
        ordering = ['-updated_at']
        unique_together = ['listing', 'buyer']


class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages', verbose_name='Conversation')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages', verbose_name='Expéditeur')
    content = models.TextField(verbose_name='Contenu')
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False, verbose_name='Lu')

    def __str__(self):
        return f"Message de {self.sender.username}"

    class Meta:
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'
        ordering = ['created_at']

