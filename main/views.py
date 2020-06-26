# Create your views here.
#import
import requests,json
from .models import Book,User
from django.views import generic
from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import LoginForm,UserCreationForm,SignUpForm,LendBookForm,PreviewForm,PostSearchForm
from django.contrib.auth.views import (LoginView, LogoutView)
from django.shortcuts import render, redirect,get_object_or_404
from django.db.models import Q
class BookList(generic.ListView):
    model = Book
    ordering ='-created_at'
    template_name = 'contents/book_list.html'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        form = PostSearchForm(self.request.GET)
        if form.is_valid():
            book_title= form['key_word'].value()
            if book_title:
                queryset = queryset.filter(Q(book_title__icontains=book_title) | Q(description__icontains=book_title))
            return queryset
        
class Published(generic.ListView):
    model = User
    ordering ='-created_at'
    template_name = 'contents/published.html'
class Profile(generic.TemplateView):
    model = User
    template_name = 'contents/profile.html'
class Login(LoginView):
    form_class = LoginForm
    template_name = 'entry/login.html'
class Logout(LogoutView):
    template_name = 'contents/book_list.html'

class Registration(generic.CreateView):
    model = Book
    form_class = PreviewForm
    
    def form_valid(self,form):
        form = form.save(commit=False)
        form.lend_user_id =self.request.user.id
        form.save()
        return redirect('main:book_list')


class CreateUser(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('main:login')
    template_name = 'entry/sign_up.html'


def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.error(request,'新規登録完了しました')
            return redirect('main:login')
    else:
        form = SignUpForm()
    return render(request, 'entry/sign_up.html', {'form': form})

def BookDelete(request,pk):
    book = get_object_or_404(Book,pk=pk)
    book.delete()
    messages.error(request,'書籍を削除しました')
    return redirect('main:published')

def BookAgain(request,pk):
    book = get_object_or_404(Book,pk=request.user.pk)
    user = get_object_or_404(User,user=book.username)
    print(book)
    print(user)
    book.lend = "True"
    user.borrow = "True" 
    user.save()
    book.save()
    messages.error(request,'再掲載しました')
    return redirect('main:published')


def BookLend(request,pk):
    book = get_object_or_404(Book,pk=pk)
    if book.lend:
        if request.user.borrow:
            user = get_object_or_404(User,pk=request.user.pk)
            user.borrow = "False"
            book.lend = "False"
            book.user_name = request.user.username
            book.user_email= request.user.email
            user.save()
            book.save()
            messages.error(request,'申請が完了しました')
            return redirect('main:book_list')
        else:
            messages.error(request,'一度に借りられるのは一冊までです')
            return redirect('main:book_list')
    else:
        messages.error(request,'ただいま貸出中です再貸出までしばらくお待ちください')
        return redirect('main:book_list')

def BookCreate(request):
    if request.method == 'POST':
        form = LendBookForm(request.POST)
        if  form['isbn_code'].value():
            sbin = form['isbn_code'].value()
            data = (requests.get(f"https://www.googleapis.com/books/v1/volumes?q=isbn:{sbin}")).json()
            if not data["totalItems"] == 0 :
                try:
                    description = data["items"][0]["volumeInfo"]["description"]
                except:
                    messages.error(request,'説明を取得できませんでした。出品者側で書き換えてください')
                    description = "未取得。"
                form = PreviewForm(initial = {
                    'book_title': data["items"][0]["volumeInfo"]["title"],
                    'author_name':data["items"][0]["volumeInfo"]["authors"][0],
                    #"publication" : data["items"][0]["volumeInfo"]["publishedDate"],
                    "description" : description,
                })
                return render(request,'entry/preview.html',{'form':form})
            else:
                messages.error(request,'書籍情報を取得できませんでした。')
                return render(request,'entry/lend.html',{'form':form})
    else:
        form = LendBookForm()
    return render(request, 'entry/lend.html', {'form':form})





