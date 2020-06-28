from django.urls import path
from . import views

#import
from django.contrib.auth.decorators import login_required


app_name = 'main'

urlpatterns = [
    path('', views.BookList.as_view(),name='book_list'),
    # login
    path('signup/',views.sign_up,name='create_user'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    
    #user
    path('profile/', login_required(views.Profile.as_view()),name='profile'),
    path('published/', login_required(views.Published.as_view()),name='published'),
    path('registration/',login_required(views.Registration.as_view()),name='registration'),

    #book
    path('lend/', login_required(views.BookCreate),name='book_create'),
    path('booklend/<int:pk>/', login_required(views.BookLend),name='book_lend'),
    path('bookagain/<int:pk>/',login_required(views.BookAgain),name='book_again'),
    path('bookdelete/<int:pk>/',login_required(views.BookDelete),name='book_delete'),
    ]