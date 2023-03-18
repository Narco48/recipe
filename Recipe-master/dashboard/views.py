from django.http.response import JsonResponse
from django.shortcuts import render
from django.views import generic
from user.models import User
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
import os
from .forms import MyPasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.db.models import Q
from .models import Categories,Recipe,FavouriteRecipe
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.template.defaulttags import register
# Create your views here.

@method_decorator(login_required(login_url='/user'), name="dispatch")
class MyProfileView(generic.TemplateView):
    template_name = "my-profile.html" 
     
    def get(self,request) :
        user=User.objects.get(id=self.request.user.id)
        return render(request,self.template_name,{"user":user})
    
    def post(self,request):
      
        fullname= request.POST.get("fullname")
      
        email= request.POST.get("email")
        phone= request.POST.get("phone")
       
        if User.objects.filter(mobile_no=phone).filter(~Q(mobile_no=request.user.mobile_no)).exists():
            messages.error(request, 'Mobile Number Already taken')
            return HttpResponseRedirect(reverse('My-Account:myaccount'))
        if User.objects.filter(email=email).filter(~Q(email=request.user.email)).exists():
            messages.error(request, 'Email Already taken') 
            return HttpResponseRedirect(reverse('My-Account:myaccount'))
        User.objects.filter(id=request.user.id).update(
                                        fullname=fullname,
                                                email=email,
                                                  mobile_no=phone)
        
                                       
        if "img" in request.FILES:
            user=request.user
            if user.img:
                image_path=user.img.path
            
                if os.path.exists(user.img.path):
                    os.remove(image_path)
                    user.img=request.FILES["img"]
                    user.save()
            else:
                user.img=request.FILES["img"]
                user.save()
            
        messages.success(request,"Profile updated successfully")
         
        return HttpResponseRedirect(reverse('dashboad:my_profile_view'))
        
            
    
@method_decorator(login_required(login_url='/user'), name="dispatch")   
class ChangePasswordView(generic.TemplateView):
    template_name = "change-password.html" 
    def post(self,request):
        form = MyPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, "Password updated successfully ")
        else:
            messages.error(request, form.errors)
		   
        return HttpResponseRedirect(reverse('dashboad:change_password_view')) 
    
@method_decorator(login_required(login_url='/user'), name="dispatch")    
class RecipeUploadView(generic.TemplateView):
    template_name = "upload-recipe.html" 

    def get_context_data(self, **kwargs) :
        context=super().get_context_data(**kwargs)
        context['categories'] =Categories.objects.all()
        return context
    
    def post(self,request):
        name= request.POST.get('name')
        photo= request.FILES['photo']
        video= request.FILES['video']
        cat= request.POST.get('category')
        description= request.POST.get('description')
        category=Categories.objects.get(id=cat)
        Recipe.objects.create(name=name,img=photo,video=video,category=category
                              ,description=description,created_by=request.user)
        messages.success(request, "Recipe uploaded successful") 
        return HttpResponseRedirect(reverse('dashboard:my_recipe_view'))
    
@method_decorator(login_required(login_url='/user'), name="dispatch")    
class MyRecipeView(generic.TemplateView):
    template_name = "my-recipes.html" 
    
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['recipes'] = Recipe.objects.filter(created_by = self.request.user)
        return context

@method_decorator(login_required(login_url='/user'), name="dispatch")    
class MyFavouriteView(generic.TemplateView):
    template_name = "my-favourite.html" 
    
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['recipes'] = FavouriteRecipe.objects.filter(user = self.request.user)
        return context
    
    
@method_decorator(login_required(login_url='/user'), name="dispatch")    
class RecipeDetailViewDashboard(generic.DetailView):
    template_name = "recipe-detail.html"
    context_object_name= 'instance' 
    queryset=Recipe.objects.all()
    
    

    
@method_decorator(login_required(login_url='/user'), name="dispatch")    
class RecipeUpdateView(generic.TemplateView):
    template_name = "update-recipe.html" 

    def get_context_data(self, **kwargs) :
        context=super().get_context_data(**kwargs)
        context['categories'] =Categories.objects.all()
        context['instance'] = Recipe.objects.get(id=self.kwargs['id'])
        return context
    
    
    
    def post(self,request,id):
        instance=Recipe.objects.get(id=id)
        name= request.POST.get('name')
        cat= request.POST.get('category')
        description= request.POST.get('description')
        category=Categories.objects.get(id=cat)
        Recipe.objects.filter(id=id).update(name=name,category=category,description=description)
        
        if 'photo' in request.FILES:
            if instance.img:
                image_path=instance.img.path
            
                if os.path.exists(instance.img.path):
                    os.remove(image_path)
                    instance.img=request.FILES["photo"]
                    instance.save()
            
        if 'video' in request.FILES:
            if instance.video:
                image_path=instance.video.path
                if os.path.exists(instance.video.path):
                    os.remove(image_path)
                    instance.video=request.FILES["video"]
                    instance.save()
            
        messages.success(request, "Recipe uploadated successful") 
        return HttpResponseRedirect(reverse('dashboard:my_recipe_view'))
    
def DeleteRecipeView(request,id):
    Recipe.objects.filter(id=id).delete()
    return JsonResponse({'status':True})

def SetStatus(request,id):
    ins=Recipe.objects.get(id=id)
 
    if ins.status:
        Recipe.objects.filter(id=id).update(status=False)
    else:
        Recipe.objects.filter(id=id).update(status=True)
    return JsonResponse({'status':True})

@method_decorator(login_required(login_url='/user'), name="dispatch")    
class SetFavourite(generic.View):
    def post(self,request):
        recipe_id = Recipe.objects.get(id=request.POST.get('value'))
        if FavouriteRecipe.objects.filter(user=request.user).filter(recipe=recipe_id).exists():
            FavouriteRecipe.objects.filter(user=request.user).filter(recipe=recipe_id).delete()
        else :
            FavouriteRecipe.objects.create(user=request.user,recipe=recipe_id)
        return JsonResponse({'status':True})
       
        
        

@register.filter(name='get_favourite_status')
def get_favourite_status(recipe,user):
    
    status=False
    if user.is_authenticated:
        if FavouriteRecipe.objects.filter(user=user).filter(recipe=recipe).exists():
            status=True
    
    return status

   