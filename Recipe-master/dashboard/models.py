from distutils.command.upload import upload
from django.db import models
from user.models import User
# Create your models here.

class Categories(models.Model):
    name=models.CharField(max_length=50)
    
    def __str__(self) -> str:
        return self.name
    
class Recipe(models.Model):
    name=models.CharField(max_length=50)
    img=models.ImageField(upload_to='recipe_photos',verbose_name="recipe photo")
    video=models.FileField(upload_to="videos" )
    category = models.ForeignKey(Categories,on_delete=models.CASCADE)
    description = models.TextField()
    created_by = models.ForeignKey(User,on_delete=models.CASCADE)
    status = models.BooleanField(default=True)
    rating_points_avg = models.FloatField(default=0,null=True,blank=True)
    no_of_user_rated_points_1 = models.PositiveIntegerField(default=0,null=True,blank=True)
    no_of_user_rated_points_2 = models.PositiveIntegerField(default=0,null=True,blank=True)
    no_of_user_rated_points_3 = models.PositiveIntegerField(default=0,null=True,blank=True)
    no_of_user_rated_points_4 = models.PositiveIntegerField(default=0,null=True,blank=True)
    no_of_user_rated_points_5 = models.PositiveIntegerField(default=0,null=True,blank=True)
    
    def __str__(self) -> str:
        return self.name
    
    
class FavouriteRecipe(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe,on_delete=models.CASCADE)
    
    
    def __str__(self) -> str:
        return f'User:-{self.user.username} Recipe:-{self.recipe.name}'

class RecipeTips(models.Model):
    name = models.CharField(max_length=255)
    
    def __str__(self) -> str:
        return self.name
