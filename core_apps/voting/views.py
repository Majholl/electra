from django.shortcuts import render, redirect
from django.urls import reverse
from django.template.loader import render_to_string

from .models import VotePanelModel
from ..user.views import user_data




def load_votepanel_page(request):
    VotePanels = VotePanelModel.objects.all()
    content_html = render_to_string('admin/votingpanels.html', context={'votingpanels': VotePanels,})
    return render(request, template_name='admin/admindash.html', context={** user_data(request), 'content':content_html})






def add_new_vote_panel(requset):
    name = requset.POST['name']
    description = requset.POST['description']
    image = requset.FILES.get('image')
    AddVotePanle = VotePanelModel.objects.create(name = name , description=description, image=image, created_by = requset.user)
    VotePanels = VotePanelModel.objects.all()
    return redirect(reverse('VotePanels'))