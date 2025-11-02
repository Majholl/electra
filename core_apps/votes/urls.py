from django.urls import path

from .views import load_vote_panel, submit_vote
from ..user.views import load_votes_tosuper_admin



urlpatterns = [
    
    path('vote', load_votes_tosuper_admin , name='VotesSection'),
    path('vote/<int:id>', load_vote_panel, name='AllVotings'),
    path('vote/submit', submit_vote , name='SubmitVote')
    
]