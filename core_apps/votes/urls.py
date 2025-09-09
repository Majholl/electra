from django.urls import path
from .views import show_votes, show_vote



urlpatterns = [
    path('voting', show_votes, name='all-votings' ),
    path('openvotes/<int:id>', show_vote, name='votedetails')
]