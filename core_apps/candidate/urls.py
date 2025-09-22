from django.urls import path 
from ..candidate.views import addnewcandidate, submitcandidate, show_candidate_list



urlpatterns = [
    path('candidates', show_candidate_list, name='candidatelist'),
    path('candidate', addnewcandidate, name='AddNewCandidate'),
    path('submitcandidate', submitcandidate, name='SubmitCandidate')
]