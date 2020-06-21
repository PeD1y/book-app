# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views import generic
from .models import Book
#from django.urls import reverse_lazy

class BookList(generic.ListView):
    model = Book
    ordering ='-category_id'
    template_name = 'contents/book_list.html'

@login_required
def test(request):
    return render(request, 'test.html')

@login_required
def test(request):
    return render(request, 'test.html')