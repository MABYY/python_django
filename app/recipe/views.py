'''
Views for the recipe APIs
'''

from rest_framework import (
    viewsets,
    mixins,
)

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import (
    Recipe,
    Tag,
)

from recipe import serializers

class RecipeViewSet(viewsets.ModelViewSet):
    '''View for manage recipe APIs.'''
    serializer_class = serializers.RecipeDetailSerializer
    queryset = Recipe.objects.all() # Objects avalilable for this viewset
    
    authentication_classes = [TokenAuthentication] # In order to use any of the endpoints provided by this viewset
    permission_classes = [IsAuthenticated] # you need to use tokenAuth and you need to be authenticated
    
    # Make super the the recipes are filtered by the authenticated user
    # To do this, overwrite the get_queryset()
  
    def get_queryset(self):
        '''Retrieve recipes for authenticated user.'''
        return self.queryset.filter(user=self.request.user).order_by('-id')
    
    # Overwrite the get_serializer_class() used by django by default to
    # determine the class being used for a paarticular action
    
    def get_serializer_class(self):
        '''Return the serializer class for request.'''
        
        if self.action == 'list':
            return serializers.RecipeSerializer
     
        return self.serializer_class
        
    def perform_create(self, serializer):
        '''Create a new recipe.'''
        '''Overwrite the behavior for when Djando saves 
            a model in a viewset'''
        serializer.save(user=self.request.user)
    
class TagViewSet(mixins.DestroyModelMixin,
                 mixins.UpdateModelMixin,
                 mixins.ListModelMixin, 
                 viewsets.GenericViewSet):  # Add listing functionality for listin models
    
    '''Manage tags in the database.'''
    serializer_class = serializers.TagSerializer
    queryset = Tag.objects.all()
    authentication_classes = [TokenAuthentication] # In order to use any of the endpoints provided by this viewset
    permission_classes = [IsAuthenticated] # you need to use tokenAuth and you need to be authenticated

    def get_queryset(self):
        '''Filter queryset to authenticated user nad order by name.'''
        return self.queryset.filter(user=self.request.user).order_by('-name')