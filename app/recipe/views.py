'''
Views for the recipe APIs
'''

from drf_spectacular.utils import (
    extend_schema_view, 
    extend_schema,
    OpenApiParameter, 
    OpenApiTypes,
)

from rest_framework import (
    viewsets,
    mixins,
    status,
)

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import (
    Recipe,
    Tag,
    Ingredient
)

from recipe import serializers

@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                'tags',
                OpenApiTypes.STR,
                description='Comma separated list of tag IDs to filter',
            ),
            OpenApiParameter(
                'ingredients',
                OpenApiTypes.STR,
                description='Comma separated list of ingredient IDs to filter',
            ),
        ]
    )
)

@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                'assigned_only',
                OpenApiTypes.INT, enum=[0, 1],
                description='Filter by items assigned to recipes.',
            ),
        ]
    )
)

class RecipeViewSet(viewsets.ModelViewSet): # ModelViewSet works directly with models
    '''View for manage recipe APIs.'''
    serializer_class = serializers.RecipeDetailSerializer
    queryset = Recipe.objects.all() # Specify the queryset/models to be used
    
    authentication_classes = [TokenAuthentication] # In order to use any of the endpoints provided by this viewset
    permission_classes = [IsAuthenticated] # you need to use tokenAuth and you need to be authenticated
    
    # Make super the the recipes are filtered by the authenticated user
    # To do this, overwrite the get_queryset()
    
    def _params_to_ints(self,qs):
        '''Convert a list of strings to integers.'''  
        return [int(str_id) for str_id in qs.split(',')]
    
  
    def get_queryset(self): 
        """Retrieve recipes for authenticated user. Ovrewrite to filter by tags/ingredients."""
        tags = self.request.query_params.get('tags')
        ingredients = self.request.query_params.get('ingredients')
        queryset = self.queryset
        if tags:
            tag_ids = self._params_to_ints(tags)
            queryset = queryset.filter(tags__id__in=tag_ids)
        if ingredients:
            ingredient_ids = self._params_to_ints(ingredients)
            queryset = queryset.filter(ingredients__id__in=ingredient_ids)

        return queryset.filter(
            user=self.request.user
        ).order_by('-id').distinct()
    
    # Overwrite the get_serializer_class() used by django by default to
    # determine the class being used for a paarticular action
    
    def get_serializer_class(self): # When using ModelViewSet, DRF provides default action mappings, ie list, upload_image
        '''Return the serializer class for request.'''
        
        if self.action == 'list':
            return serializers.RecipeSerializer
        elif self.action == 'upload_image':
            return serializers.RecipeImageSerializer
        
        return self.serializer_class
    
    @action(methods=['POST'], detail=True, url_path='upload-image')
    def upload_image(self,request,pk=None):
        '''Upload an image to recipe.'''
        recipe = self.get_object()
        serializer = self.get_serializer(recipe, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
            
    def perform_create(self, serializer): #overwrite recipe create of viewset to set the user field
        '''Create a new recipe.'''
        '''Overwrite the behavior for when Djando saves 
            a model in a viewset'''
        serializer.save(user=self.request.user)    

class BaseRecipeAttrViewSet(mixins.DestroyModelMixin,
                            mixins.UpdateModelMixin,
                            mixins.ListModelMixin,
                            viewsets.GenericViewSet):
    """Base viewset for recipe attributes."""
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter queryset to authenticated user."""
        
        assigned_only = bool(
            int(self.request.query_params.get('assigned_only', 0))
        )
        
        queryset = self.queryset
        
        if assigned_only:
            queryset = queryset.filter(recipe__isnull=False)

        return queryset.filter(
            user=self.request.user
        ).order_by('-name').distinct()
    
class TagViewSet(BaseRecipeAttrViewSet):
    """Manage tags in the database."""
    serializer_class = serializers.TagSerializer
    queryset = Tag.objects.all()

class IngredientViewSet(BaseRecipeAttrViewSet):
    """Manage ingredients in the database."""
    serializer_class = serializers.IngredientSerializer
    queryset = Ingredient.objects.all()


# class TagViewSet(mixins.DestroyModelMixin, # Implement delete and update functionality
#                  mixins.UpdateModelMixin,
#                  mixins.ListModelMixin, 
#                  viewsets.GenericViewSet):  # Add listing functionality for listin models
    
#     '''Manage tags in the database.'''
#     serializer_class = serializers.TagSerializer
#     queryset = Tag.objects.all()
#     authentication_classes = [TokenAuthentication] # In order to use any of the endpoints provided by this viewset
#     permission_classes = [IsAuthenticated] # you need to use tokenAuth and you need to be authenticated

#     def get_queryset(self):
#         '''Filter queryset to authenticated user nad order by name.'''
#         return self.queryset.filter(user=self.request.user).order_by('-name')

    
# class IngredientViewSet(mixins.DestroyModelMixin,
#                         mixins.UpdateModelMixin,
#                         mixins.ListModelMixin, 
#                         viewsets.GenericViewSet):  # Add listing functionality for listin models
    
#     '''Manage ingredients in the database.'''
#     serializer_class = serializers.IngredientSerializer
#     queryset = Ingredient.objects.all()
#     authentication_classes = [TokenAuthentication] # Adds support to use token authentication
#     permission_classes = [IsAuthenticated] # The user must be authenticated to user this endpoint

#     def get_queryset(self):
#         '''Filter queryset to authenticated user and order by name.'''
#         return self.queryset.filter(user=self.request.user).order_by('-name')
