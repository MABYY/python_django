'''
Tests for the tahs API.
'''

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Tag
from recipe.serializers import TagSerializer

TAGS_URL = reverse('recipe:tag-list')

def detail_url(tag_id):
    '''Create and return a tag detail url.'''
    return reverse('recipe:tag-detail', args=[tag_id])

def create_user(email='user@example.com', password='testpass123'):
    '''Create and return a user.'''
    return get_user_model().objects.create_user(email=email,name="Test User" ,password=password)

class PublicTagsApiTests(TestCase):
    '''Test unauthenticated API requests.'''
    
    def setUp(self):
        self.client = APIClient()
        
    def test_auth_required(self):
        '''Test auth is required for retrieving tags.'''
        res = self.client.get(TAGS_URL)
        
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        
class PrivateTagsApiTests(TestCase):
    '''Test authenticated API requests.'''
    def setUp(self):
        self.user = create_user()
        self.client = APIClient()
        self.client.force_authenticate(self.user)
    
    def rest_retrieve_tags(self):
        '''Test retrieving list of tags.'''
        Tag.objects.create(user=self.user, name="Vegan")
        Tag.objects.create(user=self.user, name="Dessert")
        
        '''Execute the code by calling the API'''
        res= self.client.get(TAGS_URL)
        
        '''Check the result'''
        tags = Tag.objects.all().order_by('-name')
        '''Serialize the result from our query'''
        serializer = TagSerializer(tags, many=True)
        
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        
        '''Expect the response data to match that of the serializer'''
        self.assertEqual(res.data, serializer.data)
        
    def test_tags_limited_to_user(self):
        '''Test list of tags is limited to authenticated user.'''
        
        '''Create a new user and its list of tags'''
        user2=create_user(email='user2@example.com',password='test2pass123')
        Tag.objects.create(user=user2, name='Fruity')  
        Tag.objects.create(user=user2, name='Fruitybis') 
        
        '''This tag is for the authenticated user'''
        tag = Tag.objects.create(user=self.user, name='Comfort food')
        
        res = self.client.get(TAGS_URL)
        
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1) # Only one, not 2
        self.assertEqual(res.data[0]['name'], tag.name)      
        self.assertEqual(res.data[0]['id'], tag.id)
        
    
    def test_update_tag(self):
        '''Test updating a tag.'''
        
        tag = Tag.objects.create(user=self.user, name = 'After dinner')

        payload = {'name' : 'Dessert'}      
        url = detail_url(tag.id)
        
        res = self.client.patch(url, payload)
        
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        tag.refresh_from_db() # refresh database after the update is made
        self.assertEqual(tag.name, payload['name'])
        
    def test_delete_tag(self):
        '''Test deleting a tag.'''
        
        tag = Tag.objects.create(user=self.user, name = 'Breakfast')
      
        url = detail_url(tag.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        tags = Tag.objects.filter(user=self.user)
        self.assertFalse(tags.exists())