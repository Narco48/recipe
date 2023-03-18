from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.views import generic
from django.contrib import messages
from django.contrib.auth import authenticate,login, logout
from django.contrib.auth.decorators import login_required
from user.models import User
import random as r
from django.template.loader import get_template
import smtplib
import email.message
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from recipe import settings
# Create your views here.


class LoginView(generic.TemplateView):
    template_name = "login.html"  
    def post(self, request,*args, **kwargs):
         
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(request, user)
            # messages.success(request, f"Successfully logged in")  
            if request.user.is_authenticated:                       
                return HttpResponseRedirect(reverse('dashboard:my_profile_view'))
        else:
            messages.error(request, "Invalid username or password.")
      
        return render(request, "login.html") 
    
class RegisterView(generic.TemplateView):
    template_name = "register.html"  
    
    def post(self, request):
        name= request.POST.get('name')
        email= request.POST.get('email')
        username= request.POST.get('username')
        mobile_no= request.POST.get('phone')
        password= request.POST.get('password')
        gender= request.POST.get('gender')
        otp=""
        for i in range(4):
            otp+=str(r.randint(1,9))
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username Already taken')
            return HttpResponseRedirect(reverse('user:register_view'))
        if User.objects.filter(mobile_no=mobile_no).exists():
            messages.error(request, 'Mobile Number Already taken')
            return HttpResponseRedirect(reverse('user:register_view'))
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email Already taken') 
            return HttpResponseRedirect(reverse('user:register_view'))
        if gender == 'gender':
            messages.error(request, 'Gender is required') 
            return HttpResponseRedirect(reverse('user:register_view'))
        user = User(fullname=name,email = email,username=username,mobile_no=mobile_no,gender=gender)
        user.set_password(password)
        user.otp=otp
        user.save()
       
        data_content = {"otp": user.otp}

        email_content = 'email_template/email_to_new_user.html'

        email_template = get_template(email_content).render(data_content)
        reciver_email = email
       
        Subject = 'Account Verification'
        email_msg = EmailMessage(Subject, email_template, settings.EMAIL_HOST_USER, [reciver_email],
                                    reply_to=[settings.EMAIL_HOST_USER])
        email_msg.content_subtype = 'html'
        email_msg.send(fail_silently=False) 
        messages.success(request, "Verification code sent to your registered mail")
        return render(request,  "verify.html",{"email":email})
    
    
class VerifyAccountView(generic.TemplateView):
    template_name = "verify.html" 
    
    def post(self,request) :
        code=request.POST.get("code")
       
        if User.objects.filter(otp=code).exists():
            User.objects.filter(otp=code).update(is_active=True)
            messages.info(request, 'Account Verified Successfully.')
            return HttpResponseRedirect(reverse('user:login_view'))
        else:
            messages.error(request, 'Entered code is wrong')
            return render(request, "verify.html")
        
        
@login_required
def LogoutView(request):
        logout(request)
        messages.success(request, "You have successfully logged out.")
        return HttpResponseRedirect(reverse('user:login_view'))