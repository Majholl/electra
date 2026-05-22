from urllib.request import Request
import json


from django.http import JsonResponse
from django.contrib.auth import  get_user_model 
from django.shortcuts import redirect
from  django.urls import reverse
from django.db.models import Q


from ..user.models import Users


User = get_user_model()


def findOnSearchToadmin(request : Request):
    
    try:
        data_to_return = {}
        
        
        SearchInUsersToAdmin = request.body
        if len(json.loads(SearchInUsersToAdmin)) > 0 :
            user = User.objects.filter(Q(national_code__icontains = json.loads(SearchInUsersToAdmin)) )
        else :
            user = User.objects.filter(usertype='user')
            
        for i in user :
            data_to_return[i.pk] = f' کد ملی : { i.national_code } -|-  نام و ناخانوادگی : { i.first_name } { i.last_name }'
            
        return JsonResponse({'status':200 , 'data' : data_to_return})
    
 

    except Exception as err :
        print(err)
        return redirect(reverse("404-nf"))
        
   