from django.urls import path
from . import views

urlpatterns = [

    path('', views.MyProfileView.as_view(), name="my_profile_view"),
    path('change-password', views.ChangePasswordView.as_view(), name="change_password_view"),
    path('upload', views.RecipeUploadView.as_view(), name="recipe_upload_view"),
    path('update-recipe/<int:id>', views.RecipeUpdateView.as_view(), name="recipe_update_view"),
    path('my-recipe', views.MyRecipeView.as_view(), name="my_recipe_view"),
    path('my-favourite', views.MyFavouriteView.as_view(), name="my_favourite_view"),
     path('recipe-detail/<pk>', views.RecipeDetailViewDashboard.as_view(), name="recipe_detail_dashboard"),
    path('delete-data/<int:id>', views.DeleteRecipeView, name="delete_recipe"),
    path('set-status/<int:id>', views.SetStatus, name="set_status"),
    path('set-status', views.SetFavourite.as_view(), name="set_favourite"),

]