# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from .models import Book
from .forms import LoginForm
from django.contrib.auth import authenticate,login
from django.contrib.auth.views import LoginView, LogoutView  
from django.urls import reverse_lazy



class BookList(generic.ListView):
    model = Book
    ordering ='-category_id'
    template_name = 'contents/book_list.html'

class LoginRequest(LoginView):
    
    template_name='entry/login.html'
    success_url = reverse_lazy('main:book_list')


'''
def login_request(request):
    if request.method =="POST":
            username = request.POST['username']
            password = request.POST['password']
            user=authenticate(username=username,password=password )
            if user is not None:
                #messages.info(request,'Welcome Back,{}.'.format(username))
                login(request,user)
                return redirect('main:book_list')
            else:
                pass
                #messages.error(request,'some error{}.'.format(form.error_messages))

    form=LoginForm()
    return render(request
        ,"entry/login.html"
        ,{"form":form}
        )

def logout_request(request):
    logout(request)
    messages.info(request,"Logged out,please come back again.")
    return redirect('main:book_list')
'''