from django.urls import path
from . import views

urlpatterns = [

    path('', views.FindRecipeView.as_view(), name="find_recipe_view"),
    path('rating', views.RatingRecipeView.as_view(), name="rating_recipe_view"),
    path('detail/<pk>', views.RecipeDetailView.as_view(), name="recipe_detail"),

]