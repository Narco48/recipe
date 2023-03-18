from django.urls import path
from . import views

urlpatterns = [

    path('login/', views.AdminLoginView.as_view(), name="admin_login"),
    path('dashboard', views.AdminDashBoardView.as_view(), name="admin_dashboard"),
    # manage users
    path('manage-users/', views.ManageUsersView.as_view(), name="manage_users"),
    path('add-user/', views.AddUserView.as_view(), name="add_user"),
    path('update-user/<int:id>', views.UpdateUserView.as_view(), name="update_user"),
    path('delete-user/<int:id>', views.DeleteUserView.as_view(), name="delete_user"),
    
    #manage recipes
    path('manage-recipes/', views.ManageRecipeView.as_view(), name="manage_recipe"),
    path('add-recipe/', views.AddRecipeView.as_view(), name="add_recipe"),
    path('update-recipe/<int:id>', views.UpdateRecipeView.as_view(), name="update_recipe"),
    path('delete-recipe/<int:id>', views.DeleteRecipeView.as_view(), name="delete_recipe"),
    
    #manage profile
    path('profile/', views.AdminProfileView.as_view(), name="admin_profile"),
    path('admin-logout/', views.AdminLogoutView, name="admin_logout"),
    
    # manage Tips
    path('manage-tips/', views.ManageRecipeTipsView.as_view(), name="manage_tips"),
    path('add-tip/', views.AddRecipeTipView.as_view(), name="add_tip"),
    path('update-tip/<int:id>', views.UpdateRecipeTipView.as_view(), name="update_tip"),
    path('delete-tip/<int:id>', views.DeleteRecipeTipView.as_view(), name="delete_tip"),

]