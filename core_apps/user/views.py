import re
from django.template.loader import render_to_string
from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from django.urls import reverse

from django.contrib.auth import  get_user_model , login, logout

from core_apps import user

User =  get_user_model()


def user_data(request):
        profile_url = request.user.profile.url if request.user.profile else 'None'
        username = request.user.username 
        user_type = request.user.usertype 
        return {'username' : username, 'profile':profile_url, 'usertype':user_type}



def homePage(request):
    return render(request, template_name='main.html', context=None)




def LoginPage(request):
    return render(request, template_name='authentications/login.html', context=None)





def RegisterPage(request):
    return render(request, template_name='authentications/register.html', context=None)





# // TODO add messages of incorrect login details

def loginUser(request):

    if not request.POST['username'] or not request.POST['password'] : 
        return render(request, template_name='authentications/login.html', context={'EmptyValues' : 'Form is empty.'})
    try:
        user = User.objects.get(username = request.POST['username'])
    
        if user :
            if user.check_password(request.POST['password']): 
                login(request, user)
                return redirect(reverse('dashboard-superadmin'))
            else:
                return render(request, template_name='authentications/login.html', context={'UserNotFound':'Password is incorrect.'})
    
    except User.DoesNotExist:
        return render(request, template_name='authentications/login.html', context={'UserNotFound':'User does not exits.'})






def SuperAdminPage(request):
                
                return render(request, template_name='admin/admindash.html', context={** user_data(request)})





def logoutUser(request):
    logout(request)
    return redirect(reverse('AuthLogin'))






def admins_list(request, page_num = 1):
        users = User.objects.all()
        paginator = Paginator(users, 2)
        pagination_objlist = paginator.get_page(page_num)
        content_html = render_to_string('admin/admins-page.html', context={'obj_list': pagination_objlist.object_list,})
        return render(request, template_name='admin/admindash.html', context={** user_data(request), 'content':content_html})



        
        
    


















def registerUser(request):
    return render(request, template_name='main/register.html', context={})



