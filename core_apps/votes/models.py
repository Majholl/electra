
from django.db import models


from ..voting.models import VotePanelModel
from ..candidate.models import CandidateModel
from ..user.models import Users



class VotesModel(models.Model):
    vote_panel = models.ForeignKey(verbose_name='Vote panel to assign', to = VotePanelModel, on_delete=models.DO_NOTHING)
    candidate = models.ForeignKey(verbose_name='Candidate to assign', to = CandidateModel, on_delete=models.DO_NOTHING, null=True)
    user = models.ForeignKey(verbose_name='User who votes', to= Users, on_delete=models.DO_NOTHING)
    voted_at = models.DateTimeField(verbose_name='When vote added', auto_now=True)
    
    class Meta :
        verbose_name = 'Votes'
        db_table = 'votes'
        ordering = ['-voted_at']