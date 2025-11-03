#//TODO add logger for diff loggs


# PY - modules
from ast import Dict
from urllib.request import Request
import random


# DJANGO - modules
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth import  get_user_model , login, logout
from django.template.loader import render_to_string
from django.contrib.auth.hashers import make_password
from django.core.paginator import Paginator
from django.contrib import messages
from django.conf import settings


from ..votes.models import VotePanelModel
from ..user.models import Users, GroupUserAdminModel





User =  get_user_model()




def generate_code():
    return ''.join(random.choice(["0","1","2","3","4","5","6","7","8","9"]) for _ in range(6))


def user_data(request :Request) -> Dict:
    try:       
        if request.user.is_authenticated: 
            user_profile_url = request.user.profile
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
                    
                    if settings.OTP_REQUIRED and user.is_active==0:
                        login(request, user, backend='core_apps.user.authentication.AllowInactiveUserBackend')
                        return redirect(reverse('verify-user-otp-page')) 
                    
                    else:
                        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
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
        print(err)
        return redirect(reverse('500-se'))






def AdminDashboard(request :Request):
    content_html = render_to_string('admin/adminhome.html', context={** user_data(request)}, request=request)
    return render(request, template_name='admin/admindash.html', context={** user_data(request), 'content':content_html})












def load_vote_section(request):
    grusers = GroupUserAdminModel.objects.get(user = request.user)

    if request.user.usertype =='admin':
        vote_panels = VotePanelModel.objects.filter(created_by=request.user)
    elif request.user.usertype =='user':
        vote_panels = VotePanelModel.objects.filter(created_by = Users.objects.get(id = grusers.relatedtoadmin.id))
    else:
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
                
                isLimited = request.POST.get("limit_making_votepanel")
                numLimitation = request.POST.get('number_making_votepanel')
                
                user = User.objects.get(id = int(userid))
                
                if isLimited=='on' and len(numLimitation):
                    messages.add_message(request, messages.ERROR,'کاربر نمیتواند همزمان دو مقدار داشته باشد')
                    return redirect(reverse('LoadSelectedAdmin', kwargs={'id': user.id}))
                
               
                if isLimited == 'on':
                        user.allowunlimitpanelcreation = 1
                        user.maxpanelcount = 0
                else :
                    if len(numLimitation) > 0 :
                        user.maxpanelcount = int(numLimitation)

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
                isLimited = request.POST.get("limit_making_votepanel")
                numLimitation = request.POST.get('number_making_votepanel')
                
                
                if (selected_user == 'کاربران') :
                    messages.add_message(request, messages.ERROR, 'یک کاربر را از لیست انتخاب کنید')
                    return redirect(reverse('AddNewAdminList'))
                
                
                if isLimited=='on' and len(numLimitation):
                    messages.add_message(request, messages.ERROR,'کاربر نمیتواند همزمان دو مقدار داشته باشد')
                    return redirect(reverse('AddNewAdminList'))
                
                
                find_userid = selected_user.split('_')[-1]
                
                if selected_user != 'کاربران':
                    user = User.objects.get(id = find_userid)
                    
                    if isLimited == 'on':
                        user.allowunlimitpanelcreation = 1
                    else :
                        if len(numLimitation) > 0 :
                            user.maxpanelcount = int(numLimitation)
                        else:
                            messages.add_message(request, messages.ERROR, 'تعداد مجاز ساخت پنل را وارد کنید')
                            return redirect(reverse('AddNewAdminList'))
                
                    user.usertype = 'admin'
                    user.save()
                                
                return redirect(reverse('AdminsList'))
            
            
            except Exception as err:
                print(err)
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










def load_page_register_user_by_admin(request :Request):
    content_html = render_to_string('admin/users/register-user-byadmin.html', context={** user_data(request)}, request=request)
    return render(request, template_name='admin/admindash.html', context={** user_data(request), 'content':content_html})















#//TODO make it better
def register_user_by_admin(request):
    if request.method == "POST":
        first_name = request.POST.get('first-name')
        last_name = request.POST.get('last-name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if Users.objects.filter(username = username).exists() or Users.objects.filter(email= email).exists():
            messages.add_message(request, messages.ERROR,'این کاربر در سیستم وجود دارد')

            return redirect(reverse('load-page-register-user-by-admin'))
            
        create_user = Users.objects.create(username = username, email=email, first_name=first_name, last_name=last_name, password=make_password(password))
        
        if settings.OTP_REQUIRED:
            create_user.set_otp(generate_code())
            create_user.account_status='deactive'
            create_user.save()
            
        GroupUserAdminModel.objects.create(user=create_user, relatedtoadmin=request.user)
        return redirect(reverse('load-page-register-user-by-admin'))
    
    
    
    
    
def verify_otp_page(request):
    print(request.user)
    return render(request, template_name='verify-otp.html', context=None,)
    
    
    
def verify_otp(request):
    if request.method =='POST':
        print(request.user)
        
        otp_input = request.POST.get("otp-input")
        user_verify = Users.objects.get(id = request.user.id)
        print(otp_input)
        if user_verify.account_status != 'locked':
            if user_verify.otp == otp_input:
                user_verify.is_active =1
                user_verify.clear_otp
                user_verify.save()
                return redirect(reverse('UserPanel'))
            else:
                user_verify.otp_attempt_count
                messages.add_message(request, messages.INFO, 'کد تاییدیه شما اشتباه است')
                return redirect(reverse('verify-user-otp-page'))
                
                
        else:
            user_verify.otp_attempt_count
            messages.add_message(request, messages.INFO, 'اکانت شما قفل میباشد ')
            
            return redirect(reverse('verify-user-otp-page'))