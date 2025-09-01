from django.shortcuts import render, redirect
from django.urls import reverse
from ..voting.models import VotePanelModel
from ..candidate.models import CandidateModel



def addnewcandidate(request):
    votepanel = VotePanelModel.objects.all()
    return render(request, template_name='main/candidate.html', context={'votepanels': votepanel})

def submitcandidate(request):
    print(request.POST)
    
    newcandidate = CandidateModel.objects.create(name= request.POST['name'], description = request.POST['description'],
                                                 image = request.FILES.get('image'), 
                                                 created_by = request.user,)
    votepanel = [VotePanelModel.objects.get(id = request.POST['panel'])]
    newcandidate.votepanel.set(votepanel)
                                        
    return redirect(reverse('adminpage'))