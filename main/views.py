# Create your views here.
#import
import requests,json
from .models import Book,User
from django.db.models import Q
from django.views import generic
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.views import (LoginView, LogoutView)
from django.shortcuts import render, redirect,get_object_or_404
from .forms import LoginForm,UserCreationForm,SignUpForm,LendBookForm,PreviewForm,PostSearchForm

class Logout(LogoutView):
    template_name = 'contents/book_list.html'
class Profile(generic.TemplateView):
    model = User
    template_name = 'contents/profile.html'
class Published(generic.ListView):
    model = User
    template_name = 'contents/published.html'
class Login(LoginView):
    form_class = LoginForm
    template_name = 'entry/login.html'
class CreateUser(generic.CreateView):
    form_class = UserCreationForm
    template_name = 'entry/sign_up.html'
    success_url = reverse_lazy('main:login')
class Registration(generic.CreateView):
    model = Book
    form_class = PreviewForm
    
    def form_valid(self,form):
        form = form.save(commit=False)
        form.lend_user_id = self.request.user.id
        form.save()
        messages.info(self.request,'書籍登録完了しました')
        return redirect('main:book_list')

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

def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.info(request,'新規登録完了しました')
            return redirect('main:login')
    else:
        form = SignUpForm()
    return render(request, 'entry/sign_up.html', {'form': form})

def BookDelete(request,pk):
    book = get_object_or_404(Book,pk=pk)
    book.delete()
    messages.info(request,'書籍を削除しました')
    return redirect('main:published')

def BookAgain(request,pk):
    book,user= get_object_or_404(Book,pk=pk),get_object_or_404(User,username=book.user_name)
    book.lend, user.borrow = "True","True" 
    user.save(),book.save()
    messages.info(request,'再掲載しました')
    return redirect('main:published')

def BookLend(request,pk):
    print(request)
    book = get_object_or_404(Book,pk=pk)
    if book.lend:
        if request.user.borrow:
            user = get_object_or_404(User,pk=request.user.pk)
            user.borrow,book.lend = "False","False"
            book.user_name,book.user_email = request.user.username,request.user.email
            user.save(),book.save()
            messages.info(request,'申請が完了しました')
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
            data = (requests.get(f"https://www.googleapis.com/books/v1/volumes?q=isbn:{form['isbn_code'].value()}")).json()
            if not data["totalItems"] == 0 :
                try:
                    description = data["items"][0]["volumeInfo"]["description"]
                except:
                    messages.error(request,'説明を取得できませんでした。出品者側で書き換えてください')
                    description = "未取得。"
                form = PreviewForm(initial = {
                    "description" : description,
                    'book_title': data["items"][0]["volumeInfo"]["title"],
                    'author_name':data["items"][0]["volumeInfo"]["authors"][0],
                    #"publication" : data["items"][0]["volumeInfo"]["publishedDate"],
                })
                return render(request,'entry/preview.html',{'form':form})
            else:
                messages.error(request,'書籍情報を取得できませんでした。')
                return render(request,'entry/lend.html',{'form':form})
    else:
        form = LendBookForm()
    return render(request, 'entry/lend.html', {'form':form})





