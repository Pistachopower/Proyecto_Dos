from django.urls import path
from .import views

urlpatterns = [
    path('clientes',views.lista_clientes,name='lista_clientes'),
    path('vendedores',views.lista_vendedores,name='lista_vendedores'),
    path('',views.index,name='index'),
    path('registrar',views.registrar_usuario,name='registrar_usuario'),
    path('piezas',views.lista_pieza,name='lista_pieza'),
    

    
]