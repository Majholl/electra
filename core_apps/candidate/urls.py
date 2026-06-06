from django.urls import path 
from ..candidate.views import  CandidatePage, addnewcandidate, submitcandidate, LoadSelectedCandidate , RemoveCandidate



urlpatterns = [
    path('candidates', CandidatePage, name='Candidateslist'),
    path('candidates/<int:page_num>', CandidatePage, name='Candidateslist'),
    path('candidate/new', addnewcandidate, name='AddNewCandidate'),
    path('submitcandidate', submitcandidate, name='SubmitCandidate'),
    path('candidate/<int:id>/', LoadSelectedCandidate, name='ModifySelectedCandidate'),
    
    path('removedcandidate/<int:id>/', RemoveCandidate, name='RemoveCandidate' )
    
]