from django.urls import path
from . import views

#import
from django.contrib.auth.decorators import login_required


app_name = 'main'

urlpatterns = [
    path('', views.BookList.as_view(),name='book_list'),
    #book
    path('lend/', login_required(views.BookCreate),name='book_create'),
    path('booklend/<int:pk>/', login_required(views.BookLend),name='book_lend'),
    path('bookdelete/<int:pk>/',login_required(views.BookDelete),name='book_delete'),
    path('bookagain/<int:pk>/',login_required(views.BookAgain),name='book_again'),
    #user
    path('registration',login_required(views.Registration.as_view()),name='registration'),
    path('published/', login_required(views.Published.as_view()),name='published'),
    path('profile/', login_required(views.Profile.as_view()),name='profile'),
    # login
    path('logout/', views.Logout.as_view(), name='logout'),
    path('login/', views.Login.as_view(), name='login'),
    path('signup/',views.sign_up,name='create_user'),
    ]