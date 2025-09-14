from django.shortcuts import render, HttpResponse

#//TODO return admin and normal user panel when logged in 
#//TODO change not authenticated user behavior

class CheckUserRequestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user
        profile_url = user.profile.url if user.profile else 'None'
        username = user.username 
        user_type = user.usertype 

        if request.user.is_authenticated: 
            if user.usertype == 'superadmin':
                return render(request, template_name='admin/admindash.html', context={'username':username, 'profile':profile_url, 'usertype':user_type})
    
            elif user.usertype =='admin':
                return HttpResponse({'h':'1'})
            
            else :
                return HttpResponse({'h':'1'})
            
        return self.get_response(request)