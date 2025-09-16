
# PY - modules
from ast import Dict
from urllib.request import Request

# DJANGO - modules
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth import  get_user_model , login, logout
from django.template.loader import render_to_string
from django.core.paginator import Paginator



User =  get_user_model()


#// TODO add try /exception block


def user_data(request :Request) -> Dict:
        user_profile_url = request.user.profile.url if request.user.profile else 'None'
        user_username = request.user.username 
        user_user_type = request.user.usertype 
        return {'profile':user_profile_url, 'username' : user_username,  'usertype':user_user_type}




def homePage(request :Request):
    return render(request, template_name='main.html', context=None)




def LoginPage(request :Request):
        return render(request, template_name='authentications/login.html', context=None)




def loginUser(request  :Request):
    if not request.POST['username'] or not request.POST['password'] : 
        return render(request, template_name='authentications/login.html', context={'wrong_data':'Fill the form.'})
    try:
        user = User.objects.get(username = request.POST['username'])
    
        if user :
            if user.check_password(request.POST['password']): 
                login(request, user)
                return redirect(reverse('dashboard-superadmin'))
            else:
                return render(request, template_name='authentications/login.html', context={'wrong_data':'Your data is wrong.'})
         
    except User.DoesNotExist:
        return render(request, template_name='authentications/login.html', context={'wrong_data':'Your data is wrong.'})







def SuperAdminPage(request :Request):
    return render(request, template_name='admin/admindash.html', context={** user_data(request)})







def admins_list(request :Request, page_num :int =1) :
    users = User.objects.all()
    paginator = Paginator(users, 5)
    pagination_objlist = paginator.get_page(page_num)
    content_html = render_to_string('admin/admins-page.html', context={'objs_list': pagination_objlist.object_list,})
    return render(request, template_name='admin/admindash.html', context={** user_data(request), 'content':content_html})






def admininfo_list(request :Request, id :int):
    user = User.objects.get(id = id)
    content_html = render_to_string('admin/admininfo-page.html', context={'obj_list': user}, request=request)
    return render(request, template_name='admin/admindash.html', context={** user_data(request), 'content':content_html})






def modifyadmin(request :Request):
    if request.method == 'POST':
        print(request.POST)
        userid = request.POST.get('user_id')
        user_type = request.POST.get('user_type')
        acc_status = request.POST.get('acc_status')
        
        user = User.objects.get(id = int(userid))
        user.usertype = user_type
        user.account_status = acc_status
        user.save()
        
    return redirect(reverse('admininfoList', kwargs={'id': user.id}))

   











def logoutUser(request :Request):
    logout(request)
    return redirect(reverse('AuthLogin'))

        






















def RegisterPage(request :Request):
    return render(request, template_name='authentications/register.html', context=None)




def registerUser(request):
    return render(request, template_name='main/register.html', context={})



