from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('contato/', views.contato, name='contato'),
    path('produto/', views.produto, name='produto'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('login/', views.login, name='login'),
    #path('logout/', views.logout, name='logout'),
]
