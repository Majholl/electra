from django.urls import path
from .views import (VotePanelsPage, LoadSelectedVotePanel, ModifySelectedVotepanel, RemoveCandidateFromVotepanel
                    ,AddNewVotePanelPage, AddNewVotePanel,  
                    )





urlpatterns = [
    path('votepanels/', VotePanelsPage, name='VotePanels'),
    path('votepanels/<int:page_num>/', VotePanelsPage, name='VotePanels'),
    path('votepanel/<int:id>', LoadSelectedVotePanel, name='LoadSelectedVotePanel'),
    path('votepanel/modifyvotepanel/', ModifySelectedVotepanel, name='ModifySelectedVotepanel'),
    
    path('removecandidate/',RemoveCandidateFromVotepanel, name='RemoveCandidateFromVotepanel'),
    
    path('addnewpanel/', AddNewVotePanelPage, name='NewVoting'),
    path('addvoting', AddNewVotePanel, name='AddNewVotePanel'),
]