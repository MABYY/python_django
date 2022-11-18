'''
Serializers for recipe APIs
'''

from rest_framework import serializers
from core.models import (
    Recipe,
    Tag,
)

class TagSerializer(serializers.ModelSerializer):
    '''Serializer for tags.'''   
    class Meta:
        model = Tag
        fields =  ['id', 'name']
        read_only_fields = ['id'] 


class RecipeSerializer(serializers.ModelSerializer):
    '''Serializer for recipes.'''
    tags = TagSerializer(many=True,required =False) # tags will be optional in the recipe
    
    class Meta:
        model = Recipe
        fields = ['id','title','time_minutes','price','link','tags'] # add the tags field
        read_only_fields=['id']
        
    def _get_or_create_tags(self, tags, recipe):
        """Handle getting or creating tags as needed."""
        auth_user = self.context['request'].user
        for tag in tags:
            tag_obj, created = Tag.objects.get_or_create(
                user=auth_user,
                **tag,
            )
            recipe.tags.add(tag_obj)
                   
        
    def create(self,validated_data): # rewrite the create method so as to add the tags 
        '''Create a recipe.'''       # key correctly   
        tags = validated_data.pop('tags',[]) # removes tags if found in validated data
                                             # assign it to the tags variable
                                             
        recipe = Recipe.objects.create(**validated_data)
        auth_user = self.context['request'].user
        for tag in tags: # check whether the tag exists or create it, then add it to recipe
            tag_obj, created = Tag.objects.get_or_create(
                user=auth_user, 
                **tag # name = tag['name'] 
            )
            recipe.tags.add(tag_obj)
        return recipe
    
    def update(self, instance, validated_data):
        '''Update recipe.'''
        tags = validated_data.pop('tags', None)
        if tags is not None:
            instance.tags.clear()
            self._get_or_create_tags(tags, instance)
            
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance
        
class RecipeDetailSerializer(RecipeSerializer):
    '''Serializer for recipe detail view.'''
    
    class Meta(RecipeSerializer.Meta):
        fields = RecipeSerializer.Meta.fields + ['description'] 
        # Only add the detail view of the recipe
        
        