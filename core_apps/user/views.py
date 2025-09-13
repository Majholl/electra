from tkinter import NO
from django.shortcuts import render
from django.contrib.auth import  get_user_model , login, logout

User =  get_user_model()





def homePage(request):
    return render(request, template_name='main.html', context=None)



def LoginPage(request):
    return render(request, template_name='authentications/login.html', context=None)



def RegisterPage(request):
    return render(request, template_name='authentications/register.html', context=None)


















def loginUser(request):
    
    if not request.POST['username'] or  not request.POST['password'] : 
        return render(request, template_name='main/login.html', context={'EmptyValues': 'Form is empty.'})
    try:
        user = User.objects.get(username = request.POST['username'])
    
        if user :
            if user.check_password(request.POST['password']) : 
                login(request, user)
                return render(request, template_name='main/superadmin.html', context={'Username': user.username})
            else:
                return render(request, template_name='main/login.html', context={'UserNotFound':'Password is incorrect.'})
    
    except User.DoesNotExist:
        return render(request, template_name='main/login.html', context={'UserNotFound':'User does not exits.'})





def logoutUser(request):
    logout(request)
    return render(request, template_name='main/login.html', context={})






def superadminpage(request):
    return render(request, template_name='main/superadmin.html', context={'Username': request.user.username})




def registerUser(request):
    return render(request, template_name='main/register.html', context={})



