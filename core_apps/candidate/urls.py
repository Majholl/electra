from django.urls import path 
from ..candidate.views import  CandidatePage, addnewcandidate, submitcandidate, load_selected_candidate



urlpatterns = [
    path('candidates', CandidatePage, name='Candidateslist'),
    
    
    path('candidate/new', addnewcandidate, name='AddNewCandidate'),
    path('submitcandidate', submitcandidate, name='SubmitCandidate'),
    
    
    path('candidate/<int:id>/', load_selected_candidate, name='ModifySelectedCandidate')
    
    
]