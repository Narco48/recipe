from django.urls import path
from . import views

urlpatterns = [

    path('', views.LoginView.as_view(), name="login_view"),
    path('register', views.RegisterView.as_view(), name="register_view"),
    path('verify/', views.VerifyAccountView.as_view(), name="verify_account"),
    path('logout/', views.LogoutView, name="logout")

]