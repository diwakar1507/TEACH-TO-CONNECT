from django.urls import path 
from . import views
urlpatterns =[
    path('',views.home, name='home'),
    path('home',views.home, name='home'),
    path('register',views.register, name='register'),
    path('login',views.login, name='login'),
    path('logout',views.logout, name='logout'),
    path('contact',views.contact,name='contact'),
    path('about',views.about,name='about'),
    path('youtube',views.youtube,name='youtube'),
    path('books',views.books,name='books'),
    path('wikipedia',views.wiki,name='wiki')
]