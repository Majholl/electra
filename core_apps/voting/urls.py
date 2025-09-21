from django.urls import path
from .views import (votepanels_page,
                    newvoting_page, add_new_vote_panel, loadvotepanel, modify_votepanel_data
                    
                    )


urlpatterns = [
    path('voting', votepanels_page, name='VotePanels'),
    path('newvoting', newvoting_page, name='NewVoting'),
    path('addvoting', add_new_vote_panel, name='AddNewVotePanel'),
    path('panel/<int:id>', loadvotepanel, name='loadvoteingpaneldata'),
    path('modifingvoteanel', modify_votepanel_data, name='modifingvotepanel'),
    
    
]