# '''
# Database models 
# '''

from email.policy import default
from enum import unique
from unicodedata import name
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class UserManager(BaseUserManager):
    '''Manager for users.'''
    
    def create_user(self,email,password=None, **extra_fields): 
        ''' Create, dave and return a new user. '''    
        if not email:
            raise ValueError('User must have an email address.')        
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        
        return user
    
    def create_superuser(self, email, password):
        ''' Create and return a new superuser. '''
        
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self.db)
        
        return user
    
    
class User(AbstractBaseUser, PermissionsMixin):
    ''' User un system.'''
    email = models.EmailField(max_length=255,unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    objects = UserManager() 
    
    USERNAME_FIELD = 'email' 
    
    
## class UserManager:

# Since usermanager is assoicated to a model we need a way to access it.
# The way of doing this calling self.model. This is equivalent to defining  
# a new user out of the the User class. 

# The password provided is hashed and will be saved this way
# password provided optionally but can't use user if this happens // testing purposes

# extra_fields: any new keyword arguments will be passed onto the model
#               useful to define new fields will be passed onto the create_user method
#               you can automatically provide the new values to the new model

# save the user model. This using=self._db supports adding multiple databases (best practice)


## class User

# objects = UserManager() ## assign user manager to our customed user class
# USER_FIELD = 'email' ## set field used for authentication
  