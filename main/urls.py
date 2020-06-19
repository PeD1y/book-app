from django.urls import path
from . import views
#from django.contrib.auth import views as auth_views

app_name = 'main'

urlpatterns = [
    path('', views.BookList.as_view(),name='book_list'),
    path('login/', views.LoginRequest.as_view(), name='login'),
    #path('logout/', LogoutView.as_view(), name='logout'),
    #path('login/',views.login_request,name='login'),
    #path('logout/',views.logout_request,name='logout') 
    ]

        
    # path('login/',views.login, name='login'),
    # path('logout',views.logout, name='logout'),
    # path('regist',views.regist,name='regist'),
    