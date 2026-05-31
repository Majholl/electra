
from urllib.request import Request
from datetime import datetime

from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.paginator import Paginator
from django.template.loader import render_to_string
from django.utils.timezone import make_aware
from django.contrib import messages



from .models import VotePanelModel 
from ..candidate.models import CandidateModel
from ..user.views import user_data , User





def VotePanelsPage(request :Request, page_num :int =1):
    try:  
        page_num = page_num
        
        if request.user.usertype == 'superadmin':
            VotePanels = VotePanelModel.objects.all()
        else :   
            VotePanels = VotePanelModel.objects.filter(created_by = request.user.id)
        paginator = Paginator(VotePanels, 20)
        page_obj_list = paginator.get_page(page_num)
        
        context = {'objs_list': page_obj_list.object_list, 'has__page':paginator.page(page_num), 'usrtype':request.user.usertype}
        content_template = 'admin/votepanels/votepanels.html'
        content_html = render_to_string(content_template, context=context)
        
        return render(request, template_name='admin/admindash.html', context={** user_data(request), 'content':content_html})
    
    
    except Exception as err:
        print(err)
        return redirect(reverse('404-nf'))






def LoadSelectedVotePanel(request:Request, id:int):
    try:    
    
        VotePanel = VotePanelModel.objects.get(id = int(id))
        Candidates = CandidateModel.objects.filter(created_by = request.user).exclude(pk__in = VotePanel.candidate.all()).all()
        
        context = {'obj_list':VotePanel, 'obj_list_2':Candidates}
        content_template = 'admin/votepanels/modifyselectedvotepanel.html'
        content_html = render_to_string(content_template, context=context, request=request)
        
        return render(request, template_name='admin/admindash.html', context={** user_data(request), 'content':content_html})

    except Exception as err:
        print(err)
        return redirect(reverse('404-nf'))











def ModifySelectedVotepanel(request ):
    try:
        if request.method == 'POST':
            try:
                vp_id = request.POST.get('panel_id')
                vp_startdate = request.POST.get('start_date')
                vp_enddate  = request.POST.get('end_date')
                vp_status = request.POST.get("vote_status")
                vp_candidate = request.POST.getlist('candidates')
                
                candidate_ = CandidateModel.objects.filter(id__in = vp_candidate).all()
                vp_ = VotePanelModel.objects.get(id = vp_id)
                
                for i in candidate_:
                    
                    vp_.candidate.add(i.pk)
                
                
                if vp_status  in ['active', 'deactive']:
                    votestatus = 1 if vp_status == 'active' else 0
                    vp_.is_active = votestatus
                    
                            
                if vp_startdate and len(vp_startdate) > 0:
                    vp_.started_date = make_aware(datetime.strptime(vp_startdate, "%Y-%m-%dT%H:%M"))
                    
                if  vp_enddate and len(vp_enddate) > 0:
                    vp_.end_date = make_aware(datetime.strptime(vp_enddate, "%Y-%m-%dT%H:%M"))
                    
                vp_.save()    
                if  vp_startdate or vp_enddate or  vp_status != 'وضعیت پنل':
                    messages.add_message(request, messages.INFO, 'اطلاعات با موفقیت ثبت شد')
                    
                return redirect(reverse('LoadSelectedVotePanel', kwargs={'id': vp_.pk}))
            
            except Exception as err :
                print(err)
                redirect(reverse('500-se'))          
                  
        return redirect(reverse('500-se'))
    
    except Exception as err:
        print(err)
        return redirect(reverse("404-nf"))








def AddNewVotePanelPage(request):
    try:
        context = None
        content_template = 'admin/votepanels/addvotepanel.html'
        content_html = render_to_string(content_template, context=context, request=request)
        return render(request, template_name='admin/admindash.html', context={** user_data(request), 'content':content_html})
    
    except Exception as err :
        return redirect(reverse("404-nf"))

 
 





def AddNewVotePanel(request):
    try :
        
        if request.method == 'POST':
            
            name = request.POST['name']
            description = request.POST['description']
            image = request.FILES.get('image')
            vp_startdate = request.POST.get('start_date')
            vp_enddate  = request.POST.get('end_date')
            
            user = User.objects.get(id = request.user.id)                            
                                        
            if ( len(name) or len(description)) == 0 :
                messages.add_message(request, messages.INFO, 'فیلد ها نباید خالی باشد')
                return redirect(reverse('NewVoting'))
            
        
            if image is None:
                messages.add_message(request, messages.INFO, 'تصویری برای پنل انتخابات ، انتخاب کنید')
                return redirect(reverse('NewVoting'))
            
            
            if user.usertype != 'superadmin':
                
                if user.allowunlimitpanelcreation == 0 :
                    if user.maxpanelcount > 0 :
                        if (user.maxpanelcount - 1) == 0 :
                            user.allowunlimitpanelcreation = 0
                        user.maxpanelcount -=1 
                        user.save()
                    messages.add_message(request, messages.INFO, 'امکان ساخت پنل برای شما وجود ندارد ، اشتراک شما تمام شده است')
                    return redirect(reverse('NewVoting'))
                
    
                
            AddVotePanle = VotePanelModel.objects.create(name = name , description=description, image=image, created_by = request.user)
            
            if vp_startdate and len(vp_startdate) > 0:
                AddVotePanle.started_date = make_aware(datetime.strptime(vp_startdate, "%Y-%m-%dT%H:%M"))
                    
            
            if  vp_enddate and len(vp_enddate) > 0:
                AddVotePanle.end_date = make_aware(datetime.strptime(vp_enddate, "%Y-%m-%dT%H:%M"))
            AddVotePanle.save()
                    
            return redirect(reverse('VotePanels'))
        
        
        
    except Exception as err :
        print(err)
        return redirect(reverse("404-nf"))

    
    
    
    
    
    





