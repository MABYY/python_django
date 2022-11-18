'''
Tests for recipe API.
'''

from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


from rest_framework import status
from rest_framework.test import APIClient

from core.models import (
    Recipe,
    Tag,
    )

from recipe.serializers import (
    RecipeSerializer , 
    RecipeDetailSerializer,
    )

RECIPES_URL = reverse('recipe:recipe-list')

def detail_url(recipe_id):
    '''Create and return a recipe detail URL.'''
    return reverse('recipe:recipe-detail',args=[recipe_id])

def create_recipe(user,**params):
    '''Create and return a sample recipe.'''
    
    defaults = {  
        'title':'Sample Title',
        'time_minutes':22,
        'price': Decimal(5.25),
        'description':'Sample description',
        'link': 'http://example.com/recipe.pdf',
    }
    
    defaults.update(params) # it will use defaults unless provided in **params 
    
    recipe = Recipe.objects.create(user=user, **defaults)
    return recipe

def create_user (**params):
    '''Create and return new user.'''
    return get_user_model().objects.create_user(**params)
    
    
class PublicRecipeAPITests(TestCase):
    '''Test unauthenticated API requests.'''
    
    def setUp(self):
        self.client = APIClient()
        
    def test_auth_required(self):
        '''Test auth is required to call API.'''
        res = self.client.get(RECIPES_URL)
        
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)    

class PrivateRecipeAPITests(TestCase):
    '''Test authenticated API requests.'''
    
    def setUp(self):
        self.client = APIClient()
        self.user = create_user(
           email='user@example.com',
            password='testpass123',
        )
        
        self.client.force_authenticate(self.user)
        
    def test_retieve_recipies(self):
        '''Test retrieving a list of recipes.'''
        create_recipe(user=self.user)
        create_recipe(user=self.user)
        
        res = self.client.get(RECIPES_URL)
        
        recipes = Recipe.objects.all().order_by('-id')
        serializer = RecipeSerializer(recipes,many=True)
                
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
        
            
    def test_recipe_list_limited_to_user(self):
        '''Test list of recipes is limited to authenticated user.'''
        
        other_user = create_user(
          email = 'other@example.com',
          password ='password123'
        )
        create_recipe(user=other_user)
        create_recipe(user=self.user)
        
        res = self.client.get(RECIPES_URL)    
        
        recipes = Recipe.objects.filter(user=self.user)
        serializer = RecipeSerializer(recipes,many=True)
                
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
    
    def test_get_recipe_detail(self):
        '''Get recipe detail.'''  
        recipe = create_recipe(user=self.user)
        
        url= detail_url(recipe.id) 
        res = self.client.get(url)
       
        serializer = RecipeDetailSerializer(recipe)   
        self.assertEqual(res.data, serializer.data)
               
    def test_create_recipe(self):
        '''Test creating a recipe.'''
        
        payload = {
            'title': 'Sample recipe',
            'time_minutes': 30,
            'price': Decimal('5.99')
        }
        res = self.client.post(RECIPES_URL,payload)
        
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        
        recipe = Recipe.objects.get(id=res.data['id'])
        
        
        for k,v in payload.items():
            self.assertEqual(getattr(recipe,k), v)
        
        self.assertEqual(recipe.user, self.user)
    
    def test_partial_update(self):
        '''Test partial update'''
        original_link =  'http://www.example.com/recipe.pdf'
        
        recipe = create_recipe(
            user= self.user,
            title='Sample recipe title',
            link=original_link
        )
        
        payload={'title': 'New recipe title'}
        url = detail_url(recipe.id)
        res = self.client.patch(url,payload)
        
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        recipe.refresh_from_db()
        self.assertEqual(recipe.title, payload['title'])
        self.assertEqual(recipe.link, original_link)
        self.assertEqual(recipe.user, self.user)
        
    def test_full_update(self):        
        '''Test full update of recipe.'''
        
        recipe = create_recipe(
            user= self.user,
            title='Sample recipe title',
            link='http://www.example.com/recipe.pdf',
            description='Sample recipe description.'
        )
        
        payload={'title': 'New recipe title',
               'link':'http://www.newexample.com/recipe.pdf',
                'description': 'New sample recipe description.',
                'time_minutes': 10,
                'price': Decimal('2.50')
            }
        
        url = detail_url(recipe.id)
        res = self.client.put(url, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        recipe.refresh_from_db()
        
        for k, v in payload.items():
            self.assertEqual(getattr(recipe, k), v)
        self.assertEqual(recipe.user, self.user)
        
        
    def test_create_recipe_with_new_tags(self):
        '''Test creating recipe with new tags'''
        
        payload = {
            'tags': [{'name':'Thai'}, {'name':'Dinner'}],
            'title': ' Thai Prawn Curry',
            'time_minutes': 30,
            'price': Decimal('2.50'),
            'link': 'http://www.example.com',  
        }
        
        res = self.client.post(RECIPES_URL,payload, format='json') 
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        
        recipes = Recipe.objects.filter(user=self.user)
        print('recipeeeeee')
        print(recipes)
        self.assertEqual(recipes.count(),1)
        
        recipe = recipes[0],
        # print('recipeeeeee')
        # print(recipe)
        self.assertEqual(recipe.tags.count(),2)
        
        for tag in payload['tags']:
            exists = recipe.tags.filter(
                name = tag['name'],
                user = self.user,
            ).exists()
            self.assertTrue(exists)
        
    
    def test_create_recipe_with_existing_tag(self):
        '''Test creating recipe with existing tag.'''
        
        tag_indian = Tag.objects.create(user=self.user, name ='Indian')
        
        payload = {
            'title': 'Pongal',
            'time_minutes': 60,
            'price': Decimal('4.20'),
            'tags':[{'name': 'Indian'}, {'name':'Breakfast'}],
        } # since the Indian tag already exists, we expect to have only one new tag

        res = self.client.post(RECIPES_URL, payload,format='json')
    
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipes = Recipe.objects.filter(user=self.user)
        self.assertEqual(recipes.count(),1)
        recipe = recipes[0]
        self.assertEqual(recipe.tags.count(),2)
        self.assertIn(tag_indian, recipe.tags.all())
        
        for tag in payload['tags']:
            exists = recipe.tags.filter(
                name = tag['name'],
                user = self.user,
            ).exists()
            self.assertTrue(exists)

    def test_create_tag_on_update(self):
        '''Test creating tag when updating a recipe.'''
        
        recipe = create_recipe(user=self.user)
        
        payload = { 'tags': [{'name':'Lunch'}]}
        url= detail_url(recipe.id)
        res = self.client.patch(url, payload, format = 'json') # only update values provided in the payload
        
        self.assertEqual(res.status_code,status.HTTP_200_OK)
        new_tag = Tag.objects.get(user=self.user, name='Lunch')
        self.assertIn(new_tag, recipe.tags.all())
        
        
    def test_update_recipe_assing_tag(self):
        '''Test assigning an existing tag '''
        
        tag_breakfast = Tag.objects.create(user=self.user, name='Breakfast')
        recipe = create_recipe(user=self.user)
        recipe.tags.add(tag_breakfast)

        tag_lunch= Tag.objects.create(user=self.user, name='Lunch')  
        payload = {'tags':[{'name': 'Lunch'}]} # this changes the tags of the recipe completely
        url = detail_url(recipe.id)
        res = self.client.patch(url, payload, format='json')
        
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn(tag_lunch,recipe.tags.all())
        self.assertNotIn(tag_breakfast, recipe.tags.all())
        
    def test_clear_recipe_tags(self):
        tag = Tag.objects.create(user=self.user, name='Dessert')
        recipe = create_recipe(user=self.user)
        recipe.tags.add(tag)
             
        payload = {'tags':[{}]} # this changes the tags of the recipe completely
        url = detail_url(recipe.id)
        res = self.client.patch(url, payload, format='json')
        
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(recipe.tags.count(),0)
        
        