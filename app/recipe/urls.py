'''
URL mappings for the recipe app.
'''

from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter
from recipe import views

 # default router provided by Djando
router = DefaultRouter() 
# use the defalt router together with views to create 
router.register('recipes', views.RecipeViewSet) 
# routes for all the options available for that view
router.register('tags', views.TagViewSet) 

app_name = 'recipe'

urlpatterns = [
    path('', include(router.urls)),
]
