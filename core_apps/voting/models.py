from django.db import models
from os import path
from ..user.models import Users
from time import time


def  VotePanelImg(instance, filename):
    try: 
        SplitedName = path.splitext(filename)
        FileName = f'{instance.name}_{int(time())}{SplitedName[-1]}'
        return path.join('votepanelimg' , FileName)
    except Exception as err:
        print(f'Error saving vote panel img name | votepanel-id {instance.pk} | {str(err)}')


class VotePanelModel(models.Model):
    name = models.CharField(max_length=64,)
    description = models.CharField(max_length=128)
    image = models.ImageField(upload_to= VotePanelImg)
    max_candidate = models.SmallIntegerField(null=True)
    max_vote = models.BigIntegerField(null=True)
    created_by = models.ForeignKey(to=Users, on_delete= models.RESTRICT)
    started_date = created_at = models.DateTimeField('Creatation datetime', auto_now_add=True)
    end_date = created_at = models.DateTimeField('Creatation datetime', auto_now_add=True)
    is_active = models.SmallIntegerField(default=0)
    created_at = models.DateTimeField('Creatation datetime', auto_now_add=True)
    updated_at = models.DateTimeField('Last modification', auto_now=True)