from django.shortcuts import render, HttpResponse

#//TODO return admin and normal user panel when logged in 
#//TODO change not authenticated user behavior

class CheckUserRequestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user
        superadminpage =  render(request, 'main/superadmin.html', context={})
        

        if request.user.is_authenticated: 
            if user.usertype == 'superadmin':
                return superadminpage
            
            elif user.usertype =='admin':
                return HttpResponse({'h':'1'})
            
            else :
                return HttpResponse({'h':'1'})
            
        return self.get_response(request)