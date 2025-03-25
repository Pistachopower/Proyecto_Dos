from django.urls import path
from .import views

urlpatterns = [
    path('clientes',views.lista_clientes,name='lista_clientes'),
    path('',views.index,name='index'),
    path('registrar',views.registrar_usuario,name='registrar_usuario'),
    
]