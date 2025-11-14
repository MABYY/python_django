'''
URL mappings for the recipe app.
'''

from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter
from recipe import views

# Default router provided by Django
# Use the default router together with views to create 
# routes for all the options available for that view

router = DefaultRouter() 

router.register('recipes', views.RecipeViewSet) 
router.register('tags', views.TagViewSet) 
router.register('ingredients', views.IngredientViewSet) 

app_name = 'recipe'

urlpatterns = [
    path('', include(router.urls)),
]
