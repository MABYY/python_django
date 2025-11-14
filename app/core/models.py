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
    AbstractBaseUser, # Modify Django default usermodel
    PermissionsMixin, # Add permissions to usermodel
    BaseUserManager, 
)

# Function to generate file path for new recipe image
def recipe_image_file_path(instance, filename):
    ''' Generate file path for new recipe image.'''
    ext = os.path.splitext(filename)[1]  # extract the extension of the pathname
    filename = f'{uuid.uuid4()}{ext}'    # create new filename using the previous extension
    
    return os.path.join('uploads', 'recipe', filename) # generate the path ensuring the format of the os we are working on


class UserManager(BaseUserManager): 
    ''' Indicates Django how to work with the customized usermodel.'''
    def create_user(self, email,name, password=None, **extra_fields): 
    #def create_user(self, email, name, password=None): 
        ''' Create, save and return a new user. '''    
        if not email:
            raise ValueError('User must have an email address.')        
        user = self.model(email=self.normalize_email(email),name=name, **extra_fields)

        #user = self.model(email=self.normalize_email(email))
        user.set_password(password) # the pwd is hashed
        user.save(using=self._db)
        
        return user
    
    def create_superuser(self, email, name, password):
        ''' Create and return a new superuser. '''
        
        user = self.create_user(email,  name, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        
        return user
    
    
class User(AbstractBaseUser, PermissionsMixin):
    ''' User profile in the system.'''
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True, null=True)
    is_staff = models.BooleanField(default=False, null=False)
    
    objects = UserManager() # class that helps us manage the user profiles

    USERNAME_FIELD = 'email' # Define field that will be used as the username
    REQUIRED_FIELDS = ['name']


    def get_full_name(self):
        return self.name 

    def get_short_name(self):
        return self.name
 
    def __str__(self):
        '''Django uses this fc to convert the object into a string'''
        return self.email
    

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