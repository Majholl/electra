#//TODO add logger for diff loggs


# PY - modules
from ast import Dict
from urllib.request import Request


# DJANGO - modules
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth import  get_user_model , login, logout
from django.template.loader import render_to_string
from django.contrib.auth.hashers import make_password
from django.core.paginator import Paginator
from django.contrib import messages

from ..votes.models import VotePanelModel


User =  get_user_model()


def user_data(request :Request) -> Dict:
    try:
        
        if request.user.is_authenticated: 
            user_profile_url = request.user.profile.url if request.user.profile else 'None'
            user_username = request.user.username 
            user_user_type = request.user.usertype 
            return {'userauth': request.user, 'profile':user_profile_url, 'username' : user_username,  'usertype':user_user_type}
        else:
            return {'userauth': request.user}
        
    except Exception as err:
        return redirect(reverse('500-se'))




def homePage(request :Request):
    return render(request, template_name='main.html', context={** user_data(request),})




def NotFound404(request :Request):
    try:
        
        content_template = '404.html'
        content_html = render_to_string(content_template, context=None)
        userdata = user_data(request)
        
        return render(request, template_name='admin/admindash.html', context={** userdata, 'content':content_html})
    
    except Exception as err:
        return redirect(reverse('500-se'))




def ServerError500(request :Request):
    
    content_template = 'server-500.html'
    content_html = render_to_string(content_template, context=None)
    userdata = user_data(request)
    
    return render(request, template_name='admin/admindash.html', context={** userdata, 'content':content_html})




def LoginPage(request :Request):
    if request.user.is_authenticated: 
        if request.user.usertype in ['superadmin', 'admin']:

            return redirect(reverse('AdminDashboard'))
        else :
            return redirect(reverse('UserPanel'))
        
    return render(request, template_name='authentications/login.html', context={** user_data(request),})









def loginUser(request  :Request):
    try:

        try:
            user = User.objects.get(username = request.POST['username'])
        
            if user :
                if user.check_password(request.POST['password']): 
                    login(request, user)
                    
                    if user.usertype == 'user':
                        return redirect(reverse('UserPanel'))
                        
                    else:
                        return redirect(reverse('AdminDashboard'))
                    
                else:
                    messages.add_message(request, messages.INFO, 'اطلاعات وارد شده اشتباه میباشد')
                    return render(request, template_name='authentications/login.html', context={** user_data(request)})
            
        except User.DoesNotExist:
            messages.add_message(request, messages.INFO, 'اطلاعات وارد شده اشتباه میباشد')
            return render(request, template_name='authentications/login.html', context={** user_data(request),'wrong_data':'Your data is wrong.'})
    
    
    except Exception as err :
        return redirect(reverse('500-se'))






def AdminDashboard(request :Request):
    content_html = render_to_string('admin/adminhome.html', context={** user_data(request)}, request=request)
    return render(request, template_name='admin/admindash.html', context={** user_data(request), 'content':content_html})












def load_vote_section(request):
    vote_panels = VotePanelModel.objects.all()
    content_html = render_to_string('votes/vote-home.html', context={** user_data(request) , 'objs_list':vote_panels}, request=request)
    return content_html



#//TODO add paginator for vote panels to vote
def UserPanel(request :Request):
    return render(request, template_name='user/userdashborad.html', context={** user_data(request), 'content':load_vote_section(request)})





def load_votes_tosuper_admin(request :Request):
    return render(request, template_name='admin/admindash.html', context={** user_data(request), 'content':load_vote_section(request)})

















def admins_list(request :Request, page_num :int =1) :
    try :
        users = User.objects.filter(usertype__in = ['superadmin', 'admin']).exclude(id = request.user.id)
        paginator = Paginator(users, 10)
        pag_obj_list = paginator.get_page(page_num)
        
        context={'objs_list': pag_obj_list.object_list, 'has__page': paginator.page(page_num)}
        content_template = 'admin/superadmin/admins-list-page.html'
        content_html = render_to_string(content_template, context)
        
        userdata = user_data(request)
        return render(request, template_name='admin/admindash.html', context={** userdata, 'content':content_html})
    
    except Exception as err :
        return redirect(reverse("404-nf"))





def load_selected_admin(request :Request, id :int):
    try:
        user = User.objects.get(id = id)
        
        context = {'obj_list': user}
        content_template = 'admin/superadmin/modify_selected_admin.html'
        content_html = render_to_string(content_template, context, request=request)
        
        return render(request, template_name='admin/admindash.html', context={** user_data(request), 'content':content_html})
    
    except Exception as err :
        print(err)
        return redirect(reverse("404-nf"))







def modify_selected_admin(request :Request):
    try:
        
        if request.method == 'POST':
            try:
                userid = request.POST.get('user_id')
                user_type = request.POST.get('user_type')
                acc_status = request.POST.get('acc_status')
                
                user = User.objects.get(id = int(userid))
                
                if user_type in ['admin', 'superadmin', 'user']:
                    user.usertype = user_type
                    
                if acc_status in ['active', 'deactive']:
                    user.account_status = acc_status
                    
                user.save()   
                 
                if acc_status in ['active', 'deactive'] or user_type in ['admin', 'superadmin', 'user'] :
                    messages.add_message(request, messages.INFO, 'اطلاعات کاربر با موفقیت بروزرسانی شد')
 
                
                return redirect(reverse('LoadSelectedAdmin', kwargs={'id': user.id}))
            
            except Exception as err :
                redirect(reverse('500-se'))
        
        return redirect(reverse('500-se'))
    
    except Exception as err :
        return redirect(reverse("404-nf"))









   
def new_admin_list(request :Request):
    try :
        
        user = User.objects.filter(usertype='user')
        
        context = {'allusers': user}
        content_template = 'admin/superadmin/addnewadmin.html'
        content_html = render_to_string(content_template, context=context, request=request)
        
        return render(request, template_name='admin/admindash.html', context={** user_data(request), 'content':content_html}) 
    
    except Exception as err :
        return redirect(reverse("404-nf"))

 
 
 

   
def PromoteUsertoAdmin(request):
    try:
        
        if request.method =='POST':
            try:
                selected_user = request.POST.get('addnewadmin')
               
                if selected_user == 'کاربران' :
                    messages.add_message(request, messages.ERROR, 'یک کاربر را از لیست انتخاب کنید')
                    return redirect(reverse('AddNewAdminList'))
                
                find_userid = selected_user.split('_')[-1]
                
                if selected_user != 'کاربران':
                    user = User.objects.get(id = find_userid)
                    user.usertype = 'admin'
                    user.save()
                                
                return redirect(reverse('AdminsList'))
            
            
            except Exception as err:
                redirect(reverse('500-se'))    
                
        return redirect(reverse('500-se'))
    
    except Exception as err:
        print(err)
        return redirect(reverse("404-nf"))





def logoutUser(request :Request):
    logout(request)
    return redirect(reverse('AuthLogin'))

        






















def RegisterPage(request :Request):
    return render(request, template_name='authentications/register.html', context=None)



def registerUser(request):
    if request.method == "POST":
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        if User.objects.filter(username = username).exists() or User.objects.filter(email= email).exists():
            return render(request, template_name='authentications/register.html', context={'error':'user exist.'})

        create_user = User.objects.create(username = username, email=email, first_name=first_name, last_name=last_name, password=make_password(password), account_status='active')
        
        return redirect(reverse('AuthLogin'))