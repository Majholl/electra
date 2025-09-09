from django.shortcuts import render

from ..voting.models import VotePanelModel



def show_votes(request):
    vote_panels = VotePanelModel.objects.all()
    return render(request, template_name='main/votes.html', context={'allvotings': vote_panels})





def show_vote(request, id):
    VotePanel_ = VotePanelModel.objects.get(id=id)
    candidate_ = VotePanel_.candidate.all()
    return render(request, 'main/uservotes.html', context={'VotePanel_': VotePanel_, 'candidate': candidate_})



