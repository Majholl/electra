from tabnanny import verbose
from django.db import models
from os import path
from ..user.models import Users


from ..voting.models import VotePanelModel
from time import time


def CandidateImg(instance, filename):
    try: 
        SplitedName = path.splitext(filename)
        FileName = f'{instance.name}_{int(time())}{SplitedName[-1]}'
        return path.join('candidateimg' , FileName)
    except Exception as err:
        print(f'Error saving vote candidate img name | candidate-id {instance.pk} | {str(err)}')



class CandidateModel(models.Model):
    name = models.CharField('Candidate name', max_length=64,)
    description = models.CharField('Candidate description', max_length=128)
    image = models.ImageField(verbose_name='Candidate image', upload_to= CandidateImg)
    votepanel = models.ManyToManyField(verbose_name='Candidate vote panel', to = VotePanelModel, related_name='candidate')
    created_by = models.ForeignKey(verbose_name='Who created candidate', to=Users, on_delete= models.RESTRICT)
    created_at = models.DateTimeField('Creatation datetime', auto_now_add=True)
    updated_at = models.DateTimeField('Last modification', auto_now=True)
    
    class Meta:
        verbose_name = 'Candidate'
        db_table = 'candidate'
        ordering = ['-created_at']