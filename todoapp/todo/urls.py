from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signupuser, name='signupuser'),
    path('current/', views.currenttodos, name='currenttodos'),
    path('logout/', views.logoutuser, name='logoutuser'),
    path('login/', views.loginuser, name='loginuser'),
    path('create/', views.createtodo, name='createtodo'),
    path('view/<str:todo_id>', views.viewtodo, name='viewtodo'),
    path('view/<str:todo_id>/delete', views.deletetodo, name='deletetodo'),
    path('view/<str:todo_id>/complete', views.completetodo, name='completetodo'),
    path('', views.homepage, name='homepage')
]