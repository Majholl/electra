from django.shortcuts import render, redirect
from django.urls import reverse
from django.template.loader import render_to_string
from django.utils.timezone import make_aware
from datetime import datetime


from .models import VotePanelModel
from ..user.views import user_data






def votepanels_page(request):
    VotePanels = VotePanelModel.objects.all()
    content_html = render_to_string('admin/votepanels/votingpanels.html', context={'votingpanels': VotePanels,})
    return render(request, template_name='admin/admindash.html', context={** user_data(request), 'content':content_html})




def newvoting_page(request):
    content_html = render_to_string('admin/votepanels/addvotingpanel.html', context={}, request= request)
    return render(request, template_name='admin/admindash.html', context={** user_data(request), 'content':content_html})






def add_new_vote_panel(requset):
    if requset.method == 'POST':
        name = requset.POST['name']
        description = requset.POST['description']
        image = requset.FILES.get('image')
        AddVotePanle = VotePanelModel.objects.create(name = name , description=description, image=image, created_by = requset.user)
        return redirect(reverse('VotePanels'))
    
    
    
    
    
    
    
def loadvotepanel(request, id):
    VotePanel = VotePanelModel.objects.get(id = id)
    content_html = render_to_string('admin/votepanels/modifingvotepanel.html', context={'obj_list':VotePanel}, request=request)
    return render(request, template_name='admin/admindash.html', context={** user_data(request), 'content':content_html})





#//TODO check if the time is not behind now
#//TODO check if the end time is not behind the start time
def modify_votepanel_data(request ):
    if request.method == 'POST':
       
        vp_id = request.POST.get('panel_id')
        vp_ = VotePanelModel.objects.get(id = vp_id)
        vp_startdate = request.POST.get('start_date')
        vp_enddate  = request.POST.get('end_date')
        vp_status = request.POST.get("vote_status")
        
        print(vp_startdate, vp_enddate)
        
        if vp_status  in ['active', 'deactive']:
            votestatus = 1 if vp_status == 'active' else 0
            vp_.is_active = votestatus
            
                    
        if vp_startdate and len(vp_startdate) > 0:
            vp_.started_date = make_aware(datetime.strptime(vp_startdate, "%Y-%m-%dT%H:%M"))
            
        if  vp_enddate and len(vp_enddate) > 0:
            vp_.end_date = make_aware(datetime.strptime(vp_enddate, "%Y-%m-%dT%H:%M"))
            
        vp_.save()    
  
        return redirect(reverse('VotePanels'))
        
    
