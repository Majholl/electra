from django.urls import path 
from ..candidate.views import addnewcandidate, submitcandidate



urlpatterns = [
    path('AddNewCandidate', addnewcandidate, name='Add_NewCandidate'),
    path('submitcandidatetopanel', submitcandidate, name='submitcandidatetopanel')
]