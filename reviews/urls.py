from django.urls import path
from . import views

urlpatterns = [
    path('create/<int:listing_pk>/', views.create_review, name='create_review'),
    path('user/<str:username>/', views.user_reviews, name='user_reviews'),
]

