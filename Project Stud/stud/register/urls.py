from django.urls import path
from . import views
urlpatterns = [
    path('login',views.home,name = 'home'),
    path('welcome',views.home,name = 'welcome'),
    path('generated',views.generate,name='generate'),
    path('home',views.home,name='zone'),
    path('welcome',views.gen_single,name='failed'),
    path('create_account',views.create_account,name = 'create_account'),
    path('testing',views.test)
]
