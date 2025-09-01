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
    name = models.CharField(max_length=64,)
    description = models.CharField(max_length=128)
    image = models.ImageField(upload_to= CandidateImg)
    votepanel = models.ManyToManyField(to = VotePanelModel)
    created_by = models.ForeignKey(to=Users, on_delete= models.RESTRICT)
    created_at = models.DateTimeField('Creatation datetime', auto_now_add=True)
    updated_at = models.DateTimeField('Last modification', auto_now=True)