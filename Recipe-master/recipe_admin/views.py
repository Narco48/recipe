import imp
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render,redirect,get_object_or_404
from django.views import generic
from django.contrib import messages
from django.contrib.auth import authenticate,login, logout

from user.models import User
from dashboard.models import Recipe,Categories,RecipeTips
from django.db.models import Q
import os
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required

# Create your views here.
def authenticate(username=None, password=None, **kwargs):
    UserModel = User
    try:
        user = UserModel.objects.get(username=username,is_superuser=True)
    except UserModel.DoesNotExist:
        return None
    else:
        if user.check_password(password):
            return user
    return None


class AdminLoginView(generic.TemplateView):
    template_name = "recipe_admin/login.html"  
    def post(self, request,*args, **kwargs):
         
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(request, user)
            # messages.success(request, f"Successfully logged in")  
            if request.user.is_authenticated:                       
                return HttpResponseRedirect(reverse('recipe_admin:admin_dashboard'))
        else:
            messages.error(request, "Invalid username or password.")
      
        return render(request, self.template_name) 
    
@method_decorator(login_required(login_url='/admin/login'), name="dispatch")   
@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class AdminDashBoardView(generic.TemplateView):
     template_name = "recipe_admin/dashboard.html"  
     
     def get_context_data(self, **kwargs):
         context=super().get_context_data(**kwargs)
         context['total_user'] = User.objects.exclude(is_superuser=True).count()
         context['total_recipe'] = Recipe.objects.count()
         context['recipes'] = Recipe.objects.all().order_by('-id')
         return context

@method_decorator(login_required(login_url='/admin/login'), name="dispatch")   
@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch') 
class ManageUsersView(generic.TemplateView):
     template_name = "recipe_admin/manage-users.html"  
     
     def get_context_data(self, **kwargs):
         context=super().get_context_data(**kwargs)
         context['users'] = User.objects.all().exclude(is_superuser=True)
 
         return context
     
@method_decorator(login_required(login_url='/admin/login'), name="dispatch")    
@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')  
class AddUserView(generic.View):
    
    def get(self, request, *args, **kwargs):
        return render (request, 'recipe_admin/add-user.html')
    
    
    def post(self, request):
        name= request.POST.get('name')
        email= request.POST.get('email')
        username= request.POST.get('username')
        mobile_no= request.POST.get('phone')
        password= request.POST.get('password')
        gender= request.POST.get('gender')
        img = request.FILES.get('img')
      
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username Already taken')
            return HttpResponseRedirect(reverse('recipe_admin:add_user'))
        if User.objects.filter(mobile_no=mobile_no).exists():
            messages.error(request, 'Mobile Number Already taken')
            return HttpResponseRedirect(reverse('recipe_admin:add_user'))
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email Already taken') 
            return HttpResponseRedirect(reverse('recipe_admin:add_user'))
        if gender == 'gender':
            messages.error(request, 'Gender is required') 
            return HttpResponseRedirect(reverse('recipe_admin:add_user'))
        user = User(fullname=name,email = email,username=username,mobile_no=mobile_no,gender=gender)
        user.set_password(password)
        user.is_active=True
        user.img=img
        user.save()
        messages.success(request, 'User added successful')
        return HttpResponseRedirect(reverse('recipe_admin:manage_users'))
        
@method_decorator(login_required(login_url='/admin/login'), name="dispatch") 
@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')     
class UpdateUserView(generic.View):
    
    def get(self, request,id, *args, **kwargs):
        instance= User.objects.get(id=id)
        gender= ['male','female']
        return render (request, 'recipe_admin/update-user.html',{'instance':instance,'gender':gender})
    
    
    def post(self, request,id):
        instance= User.objects.get(id=id)
        gender= ['male','female']
        name= request.POST.get('name')
        email= request.POST.get('email')
 
        mobile_no= request.POST.get('phone')
        password= request.POST.get('password')
        gender= request.POST.get('gender')
        img = request.FILES.get('img')
     

        if User.objects.filter(mobile_no=mobile_no).filter(~Q(id=id)).exists():
            messages.error(request, 'Mobile Number Already taken')
            return render (request, 'recipe_admin/update-user.html',{'instance':instance,'gender':gender})
        if User.objects.filter(email=email).filter(~Q(id=id)).exists():
            messages.error(request, 'Email Already taken') 
            return render (request, 'recipe_admin/update-user.html',{'instance':instance,'gender':gender})
       
        User.objects.filter(id=id).update(fullname=name,email = email,mobile_no=mobile_no,gender=gender)
        if password:
            instance.set_password(password)
            instance.save()
        if img:
            instance.img=img
            instance.save()
        messages.success(request, 'User updated successful')
        return HttpResponseRedirect(reverse('recipe_admin:manage_users'))
    
@method_decorator(login_required(login_url='/admin/login'), name="dispatch") 
@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')     
class DeleteUserView(generic.View):
    
    def post(self, request,id):
        User.objects.filter(id=id).delete()
        messages.success(request, 'User deleted successful')
        return HttpResponseRedirect(reverse('recipe_admin:manage_users'))
    
    
##########################################################   
@method_decorator(login_required(login_url='/admin/login'), name="dispatch")   
@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch') 
class ManageRecipeView(generic.TemplateView):
    template_name = "recipe_admin/manage-recipe.html" 
    
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['recipes'] = Recipe.objects.all().order_by('-id')
        return context
    
@method_decorator(login_required(login_url='/admin/login'), name="dispatch") 
@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')    
class AddRecipeView(generic.View):
    
    def get(self, request, *args, **kwargs):
        categories = Categories.objects.all()
        return render (request, 'recipe_admin/add-recipe.html',{'categories':categories})
    
    def post(self,request):
        name= request.POST.get('name')
        photo= request.FILES['photo']
        video= request.FILES['video']
        cat= request.POST.get('category')
        description= request.POST.get('description')
        category=Categories.objects.get(id=cat)
        Recipe.objects.create(name=name,img=photo,video=video,category=category
                              ,description=description,created_by=request.user)
        messages.success(request, "Recipe added successful") 
        return HttpResponseRedirect(reverse('recipe_admin:manage_recipe'))
    

@method_decorator(login_required(login_url='/admin/login'), name="dispatch")  
@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')    
class UpdateRecipeView(generic.View):
    
    def get(self, request,id, *args, **kwargs):
        instance= Recipe.objects.get(id=id)
        categories = Categories.objects.all()
        return render (request, 'recipe_admin/update-recipe.html',{'instance':instance,'categories':categories})
    
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
        return HttpResponseRedirect(reverse('recipe_admin:manage_recipe'))

@method_decorator(login_required(login_url='/admin/login'), name="dispatch")
@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch') 
class DeleteRecipeView(generic.View):
    
    def post(self, request,id):
        Recipe.objects.filter(id=id).delete()
        messages.success(request, 'Recipe deleted successful')
        return HttpResponseRedirect(reverse('recipe_admin:manage_recipe'))





########################################################################
@method_decorator(login_required(login_url='/admin/login'), name="dispatch")
@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch') 
class AdminProfileView(generic.View):
    
    def get(self, request, *args, **kwargs):
        user= request.user
        return render (request, 'recipe_admin/profile.html',{'user':user})

    def post(self, request, *args, **kwargs):
        editprofile = request.POST.get('editprofile')
        if 'manage_profile' == editprofile:
            email = request.POST['email']
            fullname = request.POST['fullname']
            mobile_no = request.POST['mobile_no']
            gender = request.POST['gender']
            User.objects.filter(email=email).update(fullname=fullname, mobile_no=mobile_no,
                gender=gender)
            messages.success(request, "User updated successfully")
            return HttpResponseRedirect(reverse('recipe_admin:admin_profile'))

        elif 'upload_image' == editprofile:
            email = request.POST['email']
            user_instance = get_object_or_404(User, email=email.lower())
            user_instance.img = request.FILES['img']
            user_instance.save()
            messages.success(request, "User Image updated successfully")
            return redirect('recipe_admin:admin_profile')

        else:
            email = request.POST['email']
            user_instance = get_object_or_404(User, email=email.lower())
            if user_instance.check_password(request.POST["old_password"]):
                password1 = request.POST["password1"]
                password2 = request.POST["password2"]
                if password1 == password2:
                    user_instance.set_password(password2)
                    user_instance.save()
                    user = authenticate(email=email, password=password2) #<-- here!!
                    if user is not None:
                        login(request,user)
                        messages.success(request, "Password changed successfully")
                        return redirect('recipe_admin:admin_profile')
                    else:
                        return redirect('recipe_admin:admin_login')
                else:
                    messages.error(request, "New Password and Confirm Password didn't match")
                    return redirect('recipe_admin:admin_profile')
            else:
                messages.error(request, "Please Enter Correct Old Password")
                return HttpResponseRedirect(reverse('recipe_admin:admin_profile'))
            
            
@login_required
def AdminLogoutView(request):
        logout(request)
        messages.success(request, "You have successfully logged out.")
        return HttpResponseRedirect(reverse('recipe_admin:admin_login'))
    
 ##############################################################################################   
@method_decorator(login_required(login_url='/admin/login'), name="dispatch")   
@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch') 
class ManageRecipeTipsView(generic.TemplateView):
    template_name = "recipe_admin/manage-tips.html" 
    
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['tips'] = RecipeTips.objects.all().order_by('-id')
        return context
    
@method_decorator(login_required(login_url='/admin/login'), name="dispatch") 
@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')    
class AddRecipeTipView(generic.View):
    
    def get(self, request, *args, **kwargs):
        return render (request, 'recipe_admin/add-tip.html')
    
    def post(self,request):
        name= request.POST.get('name')
      
        RecipeTips.objects.create(name=name)
        messages.success(request, "Tip added successful") 
        return HttpResponseRedirect(reverse('recipe_admin:manage_tips'))
    

@method_decorator(login_required(login_url='/admin/login'), name="dispatch")  
@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')    
class UpdateRecipeTipView(generic.View):
    
    def get(self, request,id, *args, **kwargs):
        instance= RecipeTips.objects.get(id=id)
        return render (request, 'recipe_admin/update-tip.html',{'instance':instance})
    
    def post(self,request,id):
        name= request.POST.get('name')
       
        RecipeTips.objects.filter(id=id).update(name=name)
        messages.success(request, "Tip uploadated successful") 
        return HttpResponseRedirect(reverse('recipe_admin:manage_tips'))
    
    
@method_decorator(login_required(login_url='/admin/login'), name="dispatch")
@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch') 
class DeleteRecipeTipView(generic.View):
    
    def post(self, request,id):
        RecipeTips.objects.filter(id=id).delete()
        messages.success(request, 'Tip deleted successful')
        return HttpResponseRedirect(reverse('recipe_admin:manage_tips'))