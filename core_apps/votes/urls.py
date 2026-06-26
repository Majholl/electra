from django.urls import path

from .views import LoadVotePanel, submit_vote
from ..user.views import loadVotesToSuperAdmin



urlpatterns = [
    
    path('vote', loadVotesToSuperAdmin , name='VotesSection'),
    
    path('vote/<int:id>', LoadVotePanel, name='LoadVotingsToVote'),
    
    path('vote/submit', submit_vote , name='SubmitVote')
    
]