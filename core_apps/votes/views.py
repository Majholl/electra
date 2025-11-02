
from urllib.request import Request

from django.urls import reverse
from django.shortcuts import render , redirect
from django.template.loader import render_to_string
from django.contrib import messages


from ..voting.models import VotePanelModel
from ..candidate.models import CandidateModel
from .models import VotesModel
from ..user.views import user_data









def load_vote_panel(request :Request, id:int):
    
    vote_panels = VotePanelModel.objects.get(pk = int(id))
    candidate = vote_panels.candidate.all()
    context = {'obj_list':vote_panels, 'obj_list_2':candidate, 'truth_obj': False}
    content_template = 'votes/load_votepanel_tovote.html'
    
    voteds = VotesModel.objects.filter(user_id = request.user, vote_panel =vote_panels).count()
    if voteds == 0:
        context['truth_obj'] = True       
            
    content_html = render_to_string(content_template, context=context, request=request)
    
    if request.user.usertype in ['superadmin', 'admin']: 
        return render(request, template_name='admin/admindash.html', context={** user_data(request), 'content':content_html})
    
    
    
    return render(request, template_name='user/userdashborad.html', context={** user_data(request), 'content':content_html})








#//TODO redirect to status of panel
#//TODO add limitation to vote 
def submit_vote(request):
    candidate_pks = request.POST.getlist('candiname_')
    vote_pane_pk = request.POST.get('vp_pks')
    
    candidates_pks = []
    
    for i in candidate_pks:   
        pks_ = i.split('_')
        candidates_pks.append(int(pks_[-1]))
        
    vp = VotePanelModel.objects.get(id = vote_pane_pk.split('_')[1])
  

    for i in candidates_pks :
        create_vote = VotesModel.objects.create(vote_panel=vp, user=request.user)
        create_vote.candidate =  CandidateModel.objects.get(pk = i)
        create_vote.save()
    
    return redirect(reverse('UserPanel'))



