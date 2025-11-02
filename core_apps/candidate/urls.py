from django.urls import path 
from ..candidate.views import addnewcandidate, submitcandidate, show_candidate_list, load_selected_candidate



urlpatterns = [
    path('candidates', show_candidate_list, name='candidatelist'),
    
    
    path('candidate/new', addnewcandidate, name='AddNewCandidate'),
    path('submitcandidate', submitcandidate, name='SubmitCandidate'),
    
    
    path('candidate/<int:id>/', load_selected_candidate, name='ModifySelectedCandidate')
    
    
]