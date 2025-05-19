from django.urls import path
from .import views

urlpatterns = [
    path('',views.index,name='index'),
    path('clientes',views.lista_clientes,name='lista_clientes'),
    path('vendedores',views.lista_vendedores,name='lista_vendedores'),
    
    #registro de usuarios
    path('registrar',views.registrar_usuario,name='registrar_usuario'),
     
    #modelo de pieza  
    path('lista-catalogo',views.lista_catalogo,name='lista_catalogo'),
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
    
    #tabla productosTienda many to many
    path('listas-productos-tienda', views.lista_ProductosTienda,name='lista_ProductosTienda'),
    path('comprar/<int:productoTienda_id>/', views.comprar_producto_tienda, name='comprar_producto_tienda'),
    path('add-producto-tienda', views.agregar_ProductoTienda,name='agregar_ProductoTienda'),
    path('eliminar-inventario/<int:id_productoTienda>',views.productoTienda_delete,name='productoTienda_delete'),
    path('editar-inventario/<int:id_ProductoTienda>', views.editar_ProductoTienda,name='editar_ProductoTienda'),


    #búsqueda pieza
    path('buscar-pieza', views.pieza_Buscar, name='pieza_Buscar'),
    path('busqueda-avanzada-pieza', views.busqueda_avanzada_pieza, name='busqueda_avanzada_pieza'),
    
    #tabla pedidos
    path('pedidos',views.lista_pedidos,name='lista_pedidos'),
    path('crear-pedido',views.pedido_create,name='pedido_create'),
    
    #linea de pedido
    path('detalle-linea-pedido/<int:id_pedido>',views.dame_lineaPedido,name='dame_lineaPedido'),

    
    
]