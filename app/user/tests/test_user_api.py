'''
Tests for the user API
'''

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')

def create_user(**params):
    '''Create and return new user. '''
    return get_user_model().objects.create_user(**params)

class PublicUserApiTests(TestCase):
    '''Tests the public features of the user API. '''
    
    def setUp(self):
        self.client = APIClient() # create an api client to use for testing
        
    def test_create_user_success(self):
        '''Test creating a user is successful.'''
        payload = {
            'email': 'test@example.com',
            'password' : 'testpass123',
            'name' : 'Test name',
        }
        
        res = self.client.post(CREATE_USER_URL,payload) # post request to out url
        
        self.assertEqual(res.status_code, status.HTTP_201_CREATED) # assertion the user was created
        
        user = get_user_model().objects.get(email=payload['email']) # validate the new user is in the database
        
        self.assertTrue(user.check_password(payload['password'])) # validate the password os correct
        
        self.assertNotIn('password',res.data) # password is not part of the data response

    def test_user_with_email_exixts_error(self):
        '''Test error returned if user with email exits.'''
        
        payload = {
            'email': 'test@example.com',
            'password' : 'testpass123',
            'name' : 'Test name',
        }
        
        create_user(**payload) # create new user 
        res = self.client.post(CREATE_USER_URL,payload) # post request to try create a another new user with existing email
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST) # assertion the user already exists
 
    def test_password_too_short_error(self):
        '''Test error is returned pass shorter that 5 characters.'''
        
        payload = {
            'email': 'test@example.com',
            'password' : 'pw',
            'name' : 'Test name',
        }
        
        res = self.client.post(CREATE_USER_URL,payload) 
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST) 
        
        user_exists = get_user_model().objects.filter( email=payload['email']).exists() # try filtering the client
        self.assertFalse(user_exists)
 
 
    def test_create_token_for_user(self):
        '''Test generates token for valid credentials.'''
        
        user_details = {
            'name':'Test Name',
            'email':'test@example.com',
            'password':'test-user-password123'
        }
        
        create_user(**user_details)
        
        payload = {
            'email': user_details['email'],
            'password': user_details['password'],
        }
        
        res = self.client.post(TOKEN_URL, payload)
        
        print('########## RES############')
        print(res)
        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        

    def test_create_token_bad_credentials(self):
        '''Test returns error if credentials are invalid'''
        
        create_user(email='test@example.com', password='goodpass')
        payload = { 'email': 'test@example.com','password': 'badpass'}
        
        res = self.client.post(TOKEN_URL, payload)
        
        self.assertNotIn('token', res.data)
        
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST) 
        
        
    def test_create_token_balnk_password(self):
        '''Test postng a blank password returns error'''
               
        payload = {'email':'test@example.com', 'password':''}
        res = self.client.post(TOKEN_URL,payload)
        
        self.assertNotIn('token',res.data)
        self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)