
from django.contrib.auth.backends import ModelBackend

from django.contrib.auth import get_user_model


UserModel = get_user_model()



class AllowInactiveUserBackend(ModelBackend):
    def user_can_authenticate(self, user):
        # Override default behavior: allow inactive users to authenticate
        
        return True
