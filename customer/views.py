from django.shortcuts import render, redirect
from django.views.generic import View, CreateView
from customer.forms import SignUpForm, LoginForm
from django.contrib.auth import authenticate, login, logout

# Create your views here.

class SignUpView(View):
    
    template_name = 'signup.html'
    form_class = SignUpForm
    
    def get(self, request, *args, **kwargs):
        
        form = self.form_class()
        
        context = {
            'form':form
        }
        
        return render(request, self.template_name, context)
    
    
    def post(self, request, *args, **kwargs):
        
        form_data = request.POST
        form = self.form_class(form_data)
        
        if form.is_valid():
            
            form.save()
            
            return redirect('signin')
        
        context = {
            'form':form
        }
        
        return render(request, self.template_name, context)
    
class LoginView(View):
    
    template_name = 'signin.html'
    form_class = LoginForm
    
    def get(self, request, *args, **kwargs):
        
        form = self.form_class()
        
        context = {
            'form':form
        }
        
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        
        form_data = request.POST
        form = self.form_class(form_data)
        
        if form.is_valid():
            
            uname = form.cleaned_data.get('username')
            pwd = form.cleaned_data.get('password')
            
            user_obj = authenticate(request, username=uname, password=pwd)
            
            if user_obj:
                
                login(request, user_obj)
                print(request.user)
                return redirect('index')
            
        context = {
            'form':form
        }
        
        return render(request, self.template_name, context)
    
    
class LogoutView(View):
    
    def get(self, request, *args, **kwargs):
        
        logout(request)
        
        return redirect('index')


class IndexView(View):
    
    template_name = 'index.html'
    
    def get(self, request, *args, **kwargs):
        
        return render(request, self.template_name)