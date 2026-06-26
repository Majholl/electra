#//TODO add logger for diff loggs


# PY - modules
from ast import Dict
from urllib.request import Request
import random , json


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
            
            path = request.path.removeprefix('/').removesuffix('/')
            if path == 'dashboard': 
                userloaction = 'اصلی'
            elif path == 'admins':
                userloaction = 'ادمین ها'
            elif path == 'votepanels':
                userloaction = 'پنل های انتخابات'
            elif path == 'candidates':
                userloaction = 'نامزد های انتخابات'
            else:
                userloaction = 'رای گیری '

            return {'userauth': request.user, 
                    'profile':user_profile_url,
                    'username' : user_username,
                    'usertype':user_user_type,
                    'userlocation': userloaction
                    }
        
        else:
            
            return {'userauth': request.user}
        
    except Exception as err:
        
        return redirect(reverse('500-se'))




def NotFound404(request :Request):
    try:
        
        content_template = 'errors/nf-404.html'
        content_html = render_to_string(content_template, context=None)
        userdata = user_data(request)
        
        return render(request, template_name='admin/admindash.html', context={** userdata, 'content':content_html})
    
    except Exception as err:
        return redirect(reverse('500-se'))




def ServerError500(request :Request):
    return render(request, template_name='errors/server-500.html', context=None)








def homePage(request :Request):
    return render(request, template_name='main.html', context={** user_data(request),})







def LoginPage(request :Request):
    try:
        if request.user.is_authenticated: 
            
            if request.user.usertype in ['superadmin', 'admin']:
                return redirect(reverse('AdminDashboard'))
            
            else :
                return redirect(reverse('UserPanel'))
            
        return render(request, template_name='authentications/login.html', context={** user_data(request),})
    
    except Exception as err:
        return redirect(reverse('500-se'))






def logoutUser(request :Request):
    logout(request)
    return redirect(reverse('AuthLogin'))

        






def AdminDashboard(request :Request):
    content_html = render_to_string('admin/adminshomepage.html', context={** user_data(request)}, request=request)
    return render(request, template_name='admin/admindash.html', context={** user_data(request), 'content':content_html})






def UserPanel(request :Request):
    return render(request, template_name='user/userdashborad.html', context={** user_data(request), 'content':loadVoteSection(request)})







def loginUser(request  :Request):
    try:
        
        username_field = request.POST.get('username_field')
        password = request.POST.get('password')
        userFound =  Users.objects.get(national_code = str(username_field)) if username_field.isdigit() else User.objects.get(username= username_field)
        if userFound :
            if userFound.check_password(password): 
                if settings.OTP_REQUIRED :
                    if userFound.is_active == 0:
                        login(request, userFound, backend='core_apps.user.authentication.AllowInactiveUserBackend')
                        return redirect(reverse('verify-user-otp-page')) 
                    
                    
                login(request, userFound, backend='django.contrib.auth.backends.ModelBackend')
                
                if userFound.usertype == 'user':
                    return redirect(reverse('UserPanel')) 
                else:
                    return redirect(reverse('AdminDashboard'))
                            
            else:
                messages.add_message(request, messages.INFO, 'رمز وارد شده اشتباه میباشد')
                return render(request, template_name='authentications/login.html', context=None)
               
    except User.DoesNotExist:
        messages.add_message(request, messages.INFO, 'اطلاعات وارد شده اشتباه میباشد')
        return render(request, template_name='authentications/login.html', context={** user_data(request),'wrong_data':'Your data is wrong.'})
    
    
    except Exception as err :
        print(err)
        return redirect(reverse('500-se'))






#//TODO add paginator for vote panels to vote

def loadVotesToSuperAdmin(request :Request):
    return render(request, template_name='admin/admindash.html', context={** user_data(request), 'content':loadVoteSection(request)})


def loadVoteSection(request  :Request):
    
    if request.user.usertype =='admin':
        vote_panels = VotePanelModel.objects.filter(created_by=request.user)
        
    elif request.user.usertype =='user':
        grusers = GroupUserAdminModel.objects.get(user = request.user)
        vote_panels = VotePanelModel.objects.filter(created_by = Users.objects.get(id = grusers.relatedtoadmin.id))
    else:
        vote_panels = VotePanelModel.objects.all()
        
    content_html = render_to_string('votes/votelists.html', context={** user_data(request) , 'objs_list':vote_panels}, request=request)
    return content_html












# SuperAdmin adding & modifying  admins pages

def registerNewAdmin(request):
    try :
        
        context = {}
        content_template = 'admin/superadmin/registernewadmin.html'
        content_html = render_to_string(content_template, context=context, request=request)
        
        return render(request, template_name='admin/admindash.html', context={** user_data(request), 'content':content_html}) 
    
    except Exception as err :
        return redirect(reverse("404-nf"))

 
 
 
 
 
def submitRegisterNewAdmin(request):
    try:
        
        nationalCode = request.POST.get("national_code")
        firstName = request.POST.get("first_name")
        lastName = request.POST.get("last_name")
        email = request.POST.get("email")
        phoneNumber = request.POST.get("phone_number")
        passWord = make_password(nationalCode)
        
        if (len(nationalCode))  == 0 or len(phoneNumber) == 0 :
            messages.add_message(request, messages.ERROR, 'فیلد ها نباید خالی باشند')
            return redirect(reverse("RegisterNewAdmin"))
        
        user = Users.objects.create(national_code=nationalCode,
                                    first_name=firstName,
                                    last_name=lastName,
                                    email=email,
                                    phone_number=phoneNumber,
                                    usertype='admin',
                                    password=passWord,
                                    account_status='deactive',
                                    is_active=0)
        if user:
            user.set_otp(generate_code())
            return redirect(reverse('AdminsList'))
    
    except Exception as err :
        print(err)
        return redirect(reverse("404-nf"))












def adminsList(request :Request, page_num :int =1) :
    try :
        users = User.objects.filter(usertype__in = ['superadmin', 'admin']).exclude(id = request.user.id)
        paginator = Paginator(users, 10)
        pag_obj_list = paginator.get_page(page_num)
        
        context={'objs_list': pag_obj_list.object_list, 'has__page': paginator.page(page_num)}
        content_template = 'admin/superadmin/admins.html'
        content_html = render_to_string(content_template, context)
        
        userdata = user_data(request)
        return render(request, template_name='admin/admindash.html', context={** userdata, 'content':content_html})
    
    except Exception as err :
        return redirect(reverse("404-nf"))





def loadSelectedAdmin(request :Request, id :int):
    try:
        user = User.objects.get(national_code  = id)
        
        context = {'obj_list': user}
        content_template = 'admin/superadmin/modifyselectedadmin.html'
        content_html = render_to_string(content_template, context, request=request)
        
        return render(request, template_name='admin/admindash.html', context={** user_data(request), 'content':content_html})
    
    except Exception as err :
        return redirect(reverse("404-nf"))




def modifySelectedAdmin(request :Request):
    try:
        
        if request.method == 'POST':
            try:
                userid = request.POST.get('user_id')
                user_type = request.POST.get('user_type')
                acc_status = request.POST.get('acc_status')
                
                isLimited = request.POST.get("limit_making_votepanel_on")
                notLimited = request.POST.get("limit_making_votepanel_off")
                numLimitation = request.POST.get('number_making_votepanel')

                user = User.objects.get(id = int(userid))
                
                if isLimited=='on' and len(numLimitation):
                    messages.add_message(request, messages.ERROR,'کاربر نمیتواند همزمان دو مقدار داشته باشد')
                    return redirect(reverse('LoadSelectedAdmin', kwargs={'id': user.national_code}))
                
               
                if notLimited == 'on':
                    user.allowunlimitpanelcreation = 1
                    user.maxpanelcount = 0
                    
                else :
                    if len(numLimitation) > 0 :
                        user.allowunlimitpanelcreation = 0
                        user.maxpanelcount = int(numLimitation)    
                   
                        
                if isLimited =='on':
                    user.allowunlimitpanelcreation = 0


                if user_type in ['admin', 'superadmin', 'user']:
                    user.usertype = user_type
                    
                if acc_status in ['active', 'deactive']:
                    user.account_status = acc_status
                    
                    
                user.save() 
                
                if acc_status in ['active', 'deactive'] or user_type in ['admin', 'superadmin', 'user']  or isLimited =='on' or notLimited == 'on':
                    messages.add_message(request, messages.INFO, 'اطلاعات کاربر با موفقیت بروزرسانی شد')
                    

                return redirect(reverse('LoadSelectedAdmin', kwargs={'id': user.national_code}))

            
            except Exception as err :
                redirect(reverse('500-se'))
        
        
        return redirect(reverse('500-se'))
    
    except Exception as err :
        return redirect(reverse("404-nf"))





   
def newAdminList(request :Request):
    
    try :
        
        user = User.objects.filter(usertype='user')
        
        context = {'allusers': user , }
        content_template = 'admin/superadmin/addnewadmin.html'
        content_html = render_to_string(content_template, context=context, request=request)
        
        return render(request, template_name='admin/admindash.html', context={** user_data(request), 'content':content_html}) 
    
    except Exception as err :
        return redirect(reverse("404-nf"))

 
 
 
   
def promoteUserToAdmin(request):
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

# End section


















def LoadAddUserPage_byAdmin(request :Request):
    try:
        
        content_template = 'admin/users/registeruserbyadmin.html'
        grusers = GroupUserAdminModel.objects.filter(relatedtoadmin = request.user).all()
        
        content_html = render_to_string(content_template, context=None)
        userdata = user_data(request)
        content_html = render_to_string(content_template, context={** userdata, 'obj_list':grusers}, request=request)
        
        return render(request, template_name='admin/admindash.html', context={** user_data(request), 'content':content_html})

    except Exception as err:
        print(err)
        return redirect(reverse("404-nf"))






def RregisterUser_byAdmin(request :Request):
    try:
        
        if request.method == "POST":
            first_name = request.POST.get('first-name')
            last_name = request.POST.get('last-name')
            national_code = request.POST.get('national-code')
            phonenumber = request.POST.get('phonenumber')
            
            user = Users.objects
            if user.filter(national_code = national_code).exists():
                messages.add_message(request, messages.ERROR,'این کاربر در سیستم وجود دارد')
                return redirect(reverse('LoadAddUserPage'))
                    
            create_user = Users.objects.create(national_code= national_code, 
                first_name=first_name, last_name=last_name,
                phone_number = phonenumber, password=make_password(national_code))
            
            if settings.OTP_REQUIRED is False :
                create_user.is_active = 1
                create_user.save()
                
            if settings.OTP_REQUIRED:
                create_user.set_otp(generate_code())
                create_user.account_status='deactive'
                create_user.save()
                
            if request.user.usertype == 'admin':    
                GroupUserAdminModel.objects.create(user=create_user, relatedtoadmin=request.user)
                
            return redirect(reverse('LoadAddUserPage'))
            
    except Exception as err:
        print(err)
        return redirect(reverse("404-nf"))

    
    
    
    
    
    

def LoadSelectedUser_byAdmin(request :Request, id :int):
    try:
        user = User.objects.get(national_code = id)
        
        context = {'obj_list': user}
        content_template = 'admin/users/modifyregisteruser.html'
        content_html = render_to_string(content_template, context, request=request)
        
        return render(request, template_name='admin/admindash.html', context={** user_data(request), 'content':content_html})
    
    except Exception as err :
        print(err)
        return redirect(reverse("404-nf"))


    
    
    
def UpdateUsersOfadmin(request:Request):
    try:
        
        if request.method == "POST":
            
                userid = request.POST.get("userid")
                profile_image = request.FILES.get("profile_image")
                fname = request.POST.get('fname')
                lastname = request.POST.get('lastname')
                email = request.POST.get('email')
                phone = request.POST.get('phone')
                password = request.POST.get('password')
                user = Users.objects.get(id=userid)
                
                if fname :
                    user.first_name = fname
                if lastname : 
                    user.last_name = lastname
                if email :
                    user.email = email
                if phone :
                    user.phone_number = phone
                if password :
                    user.password = make_password(password)                
                if profile_image :
                    user.profile = profile_image
                
                user.save()
                
        messages.add_message(request, messages.INFO, 'اطلاعات کاربر بروزرسانی شد')
        return redirect(reverse('LoadUserOfAdmin', kwargs={'id':user.national_code}))
    
    except Exception as err:
        print(err)
        return redirect(reverse('404-nf'))    
    
    
    
    
    
    
    
    
    
    
    

def verify_otp_page(request :Request):
    try :
        check_user = Users.objects.get(id = request.user.id)
        
        if check_user.is_active == 0 and check_user.otp_attempt >= 3 :
            return render(request, template_name='authentications/verify-otp.html',  context={'locked_account':True},)
        
        return render(request, template_name='authentications/verify-otp.html',  context=None,)
    
    except Exception as err:
        print(err)
        redirect(reverse('500-se'))    
                
                
    
def verify_otp(request :Request):
    if request.method =='POST':
        
        otp_input = request.POST.get("otp-input")
        
        user_verify = Users.objects.get(id = request.user.id)
        
        if user_verify.account_status != Users.AccountStatus.LOCKED:
            
            if user_verify.is_active == 0 :
                
                if user_verify.otp_attempt >= 3 :
                    return redirect(reverse('verify-user-otp-page'))     
                
                if user_verify.verify_otp_code(otp_input):
                    if user_verify.usertype == 'admin':
                        return redirect(reverse('AdminDashboard'))
                    else :
                        return redirect(reverse('UserPanel'))
                
                else:
                    user_verify.otp_attempt_count
                    messages.add_message(request, messages.INFO, 'کد تایید شما اشتباه است')
                    return redirect(reverse('verify-user-otp-page'))
                
        else:
            messages.add_message(request, messages.INFO, 'اکانت شما قفل میباشد ')
            return redirect(reverse('verify-user-otp-page'))
        
        
        
        

















def RegisterPage(request :Request):
    return render(request, template_name='authentications/register.html', context=None)