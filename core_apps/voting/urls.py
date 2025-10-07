from django.urls import path
from .views import (VotePanels_page, load_selected_votepanel, modify_selected_votepanel,
                    newvoting_page, add_new_vote_panel,  
                    )





urlpatterns = [
    path('votepanels/', VotePanels_page, name='VotePanels'),
    path('votepanels/<int:page_num>/', VotePanels_page, name='VotePanels'),
    path('votepanel/<int:id>', load_selected_votepanel, name='LoadSelectedVotePanel'),
    path('votepanel/modifyvotepanel/', modify_selected_votepanel, name='ModifySelectedVotepanel'),
    path('addnewpanel', newvoting_page, name='NewVoting'),
    path('addvoting', add_new_vote_panel, name='AddNewVotePanel'),
]