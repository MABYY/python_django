'''
URL mappings for the user API
'''

from django.urls import path
from user import views

## it maps the CREATE_USER_URL in the test_user file
app_name = 'user'  

## Define endpoins and map which views will handle each one
## It maps the CREATE_USER_URL in the test_user file 
urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create') ,
    path('token/', views.CreateTokenView.as_view(), name='token') ,
    path('me/', views.ManageUserView.as_view(), name='me'),
]    