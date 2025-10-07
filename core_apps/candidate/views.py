from django.shortcuts import render, redirect
from django.urls import reverse
from django.template.loader import render_to_string
from ..user.views import user_data


from ..voting.models import VotePanelModel
from ..candidate.models import CandidateModel




def show_candidate_list(request):
    try :
        votepanel = VotePanelModel.objects.filter(created_by = request.user)
        
        content_html = render_to_string('admin/candidate/candidate_list-page.html', context={'obj_list':votepanel}, request=request)
        return render(request, template_name='admin/admindash.html', context={** user_data(request), 'content':content_html})
    
    except Exception as err:
        print(err)
        return redirect(reverse('404-nf'))













def addnewcandidate(request):
    votepanel = VotePanelModel.objects.all()
    content_html = render_to_string('admin/candidate/candidate.html', context={'obj_list':votepanel}, request=request)
    return render(request, template_name='admin/admindash.html', context={** user_data(request), 'content':content_html})








def submitcandidate(request):
    
    
    newcandidate = CandidateModel.objects.create(name= request.POST['name'], description = request.POST['description'],
                                                 image = request.FILES.get('image'), 
                                                 created_by = request.user,)
    votepanel = [VotePanelModel.objects.get(id = request.POST['panel'])]
    newcandidate.votepanel.set(votepanel)
                                        
    return redirect(reverse('candidatelist'))