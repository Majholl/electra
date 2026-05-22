from django.urls import path
from .views import (VotePanelsPage, LoadSelectedVotePanel, modify_selected_votepanel,
                    newvoting_page, add_new_vote_panel,  
                    )





urlpatterns = [
    path('votepanels/', VotePanelsPage, name='VotePanels'),
    path('votepanels/<int:page_num>/', VotePanelsPage, name='VotePanels'),
    path('votepanel/<int:id>', LoadSelectedVotePanel, name='LoadSelectedVotePanel'),
    
    
    path('votepanel/modifyvotepanel/', modify_selected_votepanel, name='ModifySelectedVotepanel'),
    path('addnewpanel', newvoting_page, name='NewVoting'),
    path('addvoting', add_new_vote_panel, name='AddNewVotePanel'),
]