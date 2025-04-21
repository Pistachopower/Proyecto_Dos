from django.urls import path
from .import views

urlpatterns = [
    path('',views.index,name='index'),
    path('clientes',views.lista_clientes,name='lista_clientes'),
    path('vendedores',views.lista_vendedores,name='lista_vendedores'),
    
    #registro de usuarios
    path('registrar',views.registrar_usuario,name='registrar_usuario'),
     
    #modelo de pieza  
    path('piezas',views.lista_pieza,name='lista_pieza'),
    path('crear-pieza',views.pieza_create,name='pieza_create'),
    path('pieza/<int:id_pieza>',views.dame_producto,name='dame_producto'),
    path('pieza-editar/<int:id_pieza>',views.pieza_editar,name='pieza_editar'),
    path('pieza-eliminar/<int:id_pieza>',views.pieza_eliminar,name='pieza_eliminar'),
    
    #modelo tienda
    path('tienda',views.lista_tienda,name='lista_tienda'),
    path('crear-tienda',views.tienda_create,name='tienda_create'),
    path('tienda/<int:id_tienda>',views.dame_tienda,name='dame_tienda'),
    path('tienda-editar/<int:id_tienda>',views.tienda_editar,name='tienda_editar'),
    
    
    #modelo cuentaBancaria
    path('perfil-cliente/<int:id_usuario>',views.perfil_cliente,name='perfil_cliente'),
    path('crear-cuenta', views.cuenta_create, name='cuenta_create'),   
    path('cuenta-bancaria-eliminar/<int:id_usuario>',views.cuenta_delete,name='cuenta_delete'),
    path('cuenta-bancaria-editar/<int:id_cuentaaBancaria>',views.cuentaBancaria_editar,name='cuentaBancaria_editar'),
    
    #modelo vendedor
    path('perfil-vendedor/<int:id_usuario>',views.perfil_vendedor,name='perfil_vendedor'),
    path('agregar-datosVendedor', views.datosVendedor_create, name='datosVendedor_create'),

    
    

    
]