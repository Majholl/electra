from django.contrib import admin
from django.urls import path, include
from os import getenv
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path(getenv('ADMIN'), admin.site.urls),
    
    path('', include('core_apps.user.urls'), name='HomePage'),
    path('', include('core_apps.voting.urls'), name='VotingPanels'),
    path('', include('core_apps.candidate.urls'), name='Candidates'),
    path('', include('core_apps.votes.urls'), name= 'Votes')
    
]



if settings.DEBUG : 
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
