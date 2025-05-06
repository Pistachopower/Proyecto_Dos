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
    path('tienda-eliminar/<int:id_tienda>',views.tienda_eliminar,name='tienda_eliminar'),
    path('tienda-editar/<int:id_tienda>',views.tienda_editar,name='tienda_editar'),
    
    
    #modelos cliente cuentaBancaria
    path('perfil-cliente/<int:id_usuario>',views.perfil_cliente,name='perfil_cliente'),
    path('detalle-cuentaBancaria-cliente/<int:id_usuario>',views.ver_detalle_cuentaBancaria_Cliente,name='ver_detalle_cuentaBancaria_Cliente'),
    path('crear-cuenta-bancaria', views.cuentaBancaria_create, name='cuentaBancaria_create'),   
    path('cuenta-bancaria-eliminar/<int:id_cuenta>',views.cuentaBancaria_delete,name='cuentaBancaria_delete'),
    path('cuenta-bancaria-editar/<int:id_cuentaaBancaria>',views.cuentaBancaria_editar,name='cuentaBancaria_editar'),
    
    #modelo vendedor datosVendedor
    path('perfil-vendedor/<int:id_usuario>',views.perfil_vendedor,name='perfil_vendedor'),
    path('detalle-vendedor/<int:id_usuario>',views.ver_detalle_datosVendedor,name='ver_detalle_datosVendedor'),
    path('agregar-datosVendedor', views.datosVendedor_create, name='datosVendedor_create'),
    path('datos-vendedor/<int:id_Datovendedor>',views.datosVendedor_delete,name='datosVendedor_delete'),
    path('datos-vendedor-editar/<int:id_Datovendedor>',views.datosVendedor_editar,name='datosVendedor_editar'),
    
    #tabla inventario many to many
    path('listas-productos-tienda', views.lista_ProductosTienda,name='lista_ProductosTienda'),
    path('add-inventario', views.agregar_Inventario,name='agregar_Inventario'),
    path('eliminar-inventario/<int:id_Inventario>',views.datosInventario_delete,name='datosInventario_delete'),
    path('editar-inventario/<int:id_Inventario>', views.editar_Inventario,name='editar_Inventario'),
    path('ver-piezas-disponibles/<int:id_Inventario>', views.ver_Piezas_Tienda,name='ver_Piezas_Tienda'),
    
    

    #búsqueda pieza
    path('buscar-pieza', views.pieza_Buscar, name='pieza_Buscar'),
    
]