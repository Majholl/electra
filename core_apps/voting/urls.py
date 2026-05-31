from django.urls import path
from .views import (VotePanelsPage, LoadSelectedVotePanel, ModifySelectedVotepanel,
                    AddNewVotePanelPage, AddNewVotePanel,  
                    )





urlpatterns = [
    path('votepanels/', VotePanelsPage, name='VotePanels'),
    path('votepanels/<int:page_num>/', VotePanelsPage, name='VotePanels'),
    path('votepanel/<int:id>', LoadSelectedVotePanel, name='LoadSelectedVotePanel'),
    path('votepanel/modifyvotepanel/', ModifySelectedVotepanel, name='ModifySelectedVotepanel'),
    path('addnewpanel/', AddNewVotePanelPage, name='NewVoting'),
    path('addvoting', AddNewVotePanel, name='AddNewVotePanel'),
]