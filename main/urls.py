from django.contrib import admin
from django.urls import path, include
from os import getenv
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path(getenv('ADMIN'), admin.site.urls),
    path('', include('core_apps.user.urls'), name='Home-Page'),
    path('', include('core_apps.voting.urls'), name='Voting-Panel'),
    path('', include('core_apps.candidate.urls'), name='Candidate'),
    path('', include('core_apps.votes.urls'), name= 'Votes')
]



if settings.DEBUG : 
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
