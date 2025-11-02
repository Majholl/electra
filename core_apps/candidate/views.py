from django.shortcuts import render, redirect
from django.urls import reverse
from django.template.loader import render_to_string
from django.contrib import messages
from ..user.views import user_data


from ..voting.models import VotePanelModel
from ..candidate.models import CandidateModel




def show_candidate_list(request):
    try :
        candidates = CandidateModel.objects.filter(created_by = request.user).all()
        content_html = render_to_string('admin/candidate/candidate_list-page.html', context={'obj_list':candidates}, request=request)
        return render(request, template_name='admin/admindash.html', context={** user_data(request), 'content':content_html})
    
    except Exception as err:
        print(err)
        return redirect(reverse('404-nf'))











def addnewcandidate(request):
    try:
        
        content_html = render_to_string('admin/candidate/addcandidate.html', context={}, request=request)
        return render(request, template_name='admin/admindash.html', context={** user_data(request), 'content':content_html})
    
    except Exception as err:
        print(err)
        return redirect(reverse('404-nf'))






# //TODO check fields && make logic better


def submitcandidate(request):
    try:
        
        if (len(request.POST['name'] ) or len(request.POST['description'] ) or len(request.POST['image'] )) == 0 :
            messages.add_message(request, messages.INFO, 'فیلد ها نباید خالی باشد')
            return redirect(reverse('AddNewCandidate'))
        
        newcandidate = CandidateModel.objects.create(name= request.POST['name'], description = request.POST['description'],
                                                    image = request.FILES.get('image'), 
                                                    created_by = request.user,)
                                            
        return redirect(reverse('candidatelist'))

    except Exception as err:
        print(err)
        return redirect(reverse('404-nf'))















def load_selected_candidate(request, id):
    try:
        
        candidate = CandidateModel.objects.get(id = id)
        context = {'obj_list':candidate}
        content_template = 'admin/candidate/modify-selected-candidate.html'
        content_html = render_to_string(content_template, context=context, request=request)
        
        return render(request, template_name='admin/admindash.html', context={** user_data(request), 'content':content_html})

    
    except Exception as err:
        print(err)
        return redirect(reverse('404-nf'))







