from django.core.paginator import Paginator
from django.shortcuts import render


from django.contrib.auth import  get_user_model , login, logout

from core_apps import user

User =  get_user_model()





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
                profile_url = user.profile.url if user.profile else 'None'
                username = user.username 
                user_type = user.usertype 
                return render(request, template_name='admin/admindash.html', context={'username' : username, 'profile':profile_url, 'usertype':user_type})
            else:
                return render(request, template_name='authentications/login.html', context={'UserNotFound':'Password is incorrect.'})
    
    except User.DoesNotExist:
        return render(request, template_name='authentications/login.html', context={'UserNotFound':'User does not exits.'})






def logoutUser(request):
    logout(request)
    return render(request, template_name='authentications/login.html', context={})






def admins_list(request, page_num = 1):
        users = User.objects.all()
        paginator = Paginator(users, 2)
        pagination_objlist = paginator.get_page(page_num)
        return render(request, template_name='admin/admindash.html', context={'obj_list': pagination_objlist.object_list,})
        
        
    

















def SuperAdminPage(request):
    return render(request, template_name='admin/admindash.html', context={'Username': request.user.username})




def registerUser(request):
    return render(request, template_name='main/register.html', context={})



