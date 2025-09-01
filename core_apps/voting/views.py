from django.shortcuts import render, redirect
from django.urls import reverse
from .models import VotePanelModel

def load_votepanel_page(request):
    VotePanels = VotePanelModel.objects.all()
    return render(request, template_name='main/votingpanel.html', context={'votePanels':VotePanels})




def add_new_vote_panel(requset):
    name = requset.POST['name']
    description = requset.POST['description']
    image = requset.FILES.get('image')
    AddVotePanle = VotePanelModel.objects.create(name = name , description=description, image=image, created_by = requset.user)
    VotePanels = VotePanelModel.objects.all()
    return redirect(reverse('VotePanels'))