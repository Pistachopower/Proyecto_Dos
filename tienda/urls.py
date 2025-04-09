from django.urls import path
from .import views

urlpatterns = [
    path('clientes',views.lista_clientes,name='lista_clientes'),
    path('vendedores',views.lista_vendedores,name='lista_vendedores'),
    path('',views.index,name='index'),
    path('registrar',views.registrar_usuario,name='registrar_usuario'),
    path('piezas',views.lista_pieza,name='lista_pieza'),
    path('crear-pieza',views.pieza_create,name='pieza_create'),
    path('tienda',views.lista_tienda,name='lista_tienda'),
    path('crear-tienda',views.tienda_create,name='tienda_create'),
    path('pieza/<int:id_pieza>',views.dame_producto,name='dame_producto'),
    path('pieza-editar/<int:id_pieza>',views.pieza_editar,name='pieza_editar'),
    
    
    
    

    
]