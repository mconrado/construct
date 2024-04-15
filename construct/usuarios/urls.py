from django.urls import path
from . import views

urlpatterns = [
    path('cadastrar_vendedor/', views.cadastrar_vendedor, name='cadastrar_vendedor'),
    path('excluir_usuario/<str:id>/', views.excluir_usuario, name='excluir_usuario'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),

]
