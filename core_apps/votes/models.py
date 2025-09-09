from ast import mod
from turtle import mode
from django.db import models


from ..voting.models import VotePanelModel
from ..candidate.models import CandidateModel
from ..user.models import Users

class Votes(models.Model):
    vote_panel = models.ForeignKey(to = VotePanelModel, on_delete=models.DO_NOTHING)
    candidate = models.ForeignKey(to = CandidateModel, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(to= Users, on_delete=models.DO_NOTHING)
    voted_at = models.DateTimeField(auto_now=True)
    
    