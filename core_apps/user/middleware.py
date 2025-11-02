from django.utils.deprecation import MiddlewareMixin
from django.urls import reverse
from django.shortcuts import redirect


class CustomMiddleware(MiddlewareMixin):
    
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        user = request.user
        urls = [reverse('UserPanel'), reverse('AdminDashboard')]
        response = self.get_response(request)
        
        if request.path in urls and not user.is_authenticated :
            return redirect(reverse("AuthLogin"))
                
        
        return response 