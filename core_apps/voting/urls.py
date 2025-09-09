from django.urls import path
from .views import load_votepanel_page, add_new_vote_panel



urlpatterns = [
    path('Voting', load_votepanel_page, name='VotePanels'),
    path('AddNewVotePanel', add_new_vote_panel, name='AddNewVotePanel'),
    
]