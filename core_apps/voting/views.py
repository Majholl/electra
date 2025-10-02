
from urllib.request import Request
from datetime import datetime

from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.paginator import Paginator
from django.template.loader import render_to_string
from django.utils.timezone import make_aware


from .models import VotePanelModel
from ..user.views import user_data , User



#//TODO add if the its superuser to see all the votes 
#//TODO if the page has 'nt any next page return the current page

def VotePanels_page(request :Request, page_num :int =1):
    try:
        if request.user.usertype == 'supderadmin':
            VotePanels - VotePanelModel.objects.all()
            
        VotePanels = VotePanelModel.objects.filter(created_by = request.user.id)
        paginator = Paginator(VotePanels, 10)
        page_obj_list = paginator.get_page(page_num)
        
        context = {'objs_list': page_obj_list.object_list, 'has__page':paginator.page(page_num)}
        content_template = 'admin/votepanels/votepanels-list-page.html'
        content_html = render_to_string(content_template, context=context)
        
        return render(request, template_name='admin/admindash.html', context={** user_data(request), 'content':content_html})
    
    
    except Exception as err:
        print(err)
        return redirect(reverse('404-nf'))






def load_selected_votepanel(request:Request, id:int):
    try:    
    
        VotePanel = VotePanelModel.objects.get(id = int(id))
        
        context = {'obj_list':VotePanel}
        content_template = 'admin/votepanels/modify-selected-votepanel.html'
        content_html = render_to_string(content_template, context=context, request=request)
        
        return render(request, template_name='admin/admindash.html', context={** user_data(request), 'content':content_html})

    except Exception as err:
        print(err)
        return redirect(reverse('404-nf'))







#//TODO check if the time is not behind now
#//TODO check if the end time is not behind the start time
def modify_selected_votepanel(request ):
    try:
        if request.method == 'POST':
            try:
                vp_id = request.POST.get('panel_id')
                vp_startdate = request.POST.get('start_date')
                vp_enddate  = request.POST.get('end_date')
                vp_status = request.POST.get("vote_status")
                
                vp_ = VotePanelModel.objects.get(id = vp_id)
                
                if vp_status  in ['active', 'deactive']:
                    votestatus = 1 if vp_status == 'active' else 0
                    vp_.is_active = votestatus
                    
                            
                if vp_startdate and len(vp_startdate) > 0:
                    vp_.started_date = make_aware(datetime.strptime(vp_startdate, "%Y-%m-%dT%H:%M"))
                    
                if  vp_enddate and len(vp_enddate) > 0:
                    vp_.end_date = make_aware(datetime.strptime(vp_enddate, "%Y-%m-%dT%H:%M"))
                    
                vp_.save()    
        
                return redirect(reverse('LoadSelectedVotePanel', kwargs={'id': vp_.pk}))
            
            except Exception as err :
                redirect(reverse('500-se'))          
                  
        return redirect(reverse('500-se'))
    
    except Exception as err:
        return redirect(reverse("404-nf"))





















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
    
    
    
    
    
    
    





