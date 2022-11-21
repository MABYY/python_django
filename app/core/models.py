# '''
# Database models 
# '''

import uuid
import os

from django.conf import settings

from email.policy import default
from enum import unique
from unicodedata import name
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)

def recipe_image_file_path(instance, filename):
    '''Generate file path for new recipe image.'''
    ext = os.path.splitext(filename)[1]  # extract the extension of the pathname
    filename = f'{uuid.uuid4()}{ext}'    # create new filename using the previous extension
    
    return os.path.join('uploads', 'recipe', filename) # generate the path ensuring the format of the os we are working on

class UserManager(BaseUserManager):
    '''Manager for users.'''
    
    def create_user(self, email, password=None, **extra_fields): 
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
        user.save(using=self._db)
        
        return user
    
    
class User(AbstractBaseUser, PermissionsMixin):
    ''' User in the system.'''
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    objects = UserManager()

    USERNAME_FIELD = 'email'

 
    

class Recipe(models.Model): ## basic class provided by Django   
    '''Recipe object.'''
    user = models.ForeignKey(  ## it stores the user it belongs to 
        settings.AUTH_USER_MODEL,
        on_delete = models.CASCADE,
    )
    
    title = models.CharField(max_length = 255)
    description = models.TextField(blank=True)
    time_minutes = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    link = models.CharField(max_length=255,blank=True)
    tags = models.ManyToManyField('Tag') 
    ingredients=models.ManyToManyField('Ingredient') 
    image = models.ImageField(null=True, upload_to=recipe_image_file_path) # pass the upload function, don't execute it
    # we can have many recipies with many tags each
    
    def __str__(self):  ## it displays the title when listing things in the django admin 
        return self.title
    

class Tag(models.Model):
    '''Tag for filtering recipes.'''
    name = models.CharField(max_length=255)
    user = models.ForeignKey( 
            settings.AUTH_USER_MODEL,
            on_delete=models.CASCADE,
     )
    
    def __str__(self):
        return self.name

class Ingredient(models.Model):
    '''Ingredient for recipes.'''
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    def __str__(self): # string representation
        return self.name
    
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
  