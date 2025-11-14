'''
Views for the user API.
'''

from rest_framework import generics , authentication , permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings


from user.serializers import (
    UserSerializer, 
    AuthTokenSerializer,
)

class CreateUserView(generics.CreateAPIView):
    '''Create new user in the database.'''
    serializer_class = UserSerializer
    
class CreateTokenView(ObtainAuthToken): # Customize ObtainAuthToken to use our serializer
    '''Create a new auth token for user.'''
    '''We are using the OAT view provided by dajngo and customizing the serializer we created'''
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES # This is optional 
        
class ManageUserView(generics.RetrieveUpdateAPIView): 
    '''Manage the authenticated user.'''
    serializer_class = UserSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self): # '''Retrieve and return the authenticated user.''' 
        return self.request.user
    
