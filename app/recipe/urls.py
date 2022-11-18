'''
URL mappings for the recipe app.
'''

from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter
from recipe import views

router = DefaultRouter()  # default router provided by Djando
router.register('recipes', views.RecipeViewSet) # use the defalt router together with views to create # routes for all the options available for that view
router.register('tags', views.TagViewSet) 

app_name = 'recipe'

urlpatterns = [
    path('', include(router.urls))
]
