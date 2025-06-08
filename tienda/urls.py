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
    path('add-producto-tienda', views.agregar_ProductoTienda,name='agregar_ProductoTienda'),
    path('eliminar-inventario/<int:id_productoTienda>',views.productoTienda_delete,name='productoTienda_delete'),
    path('editar-inventario/<int:id_ProductoTienda>', views.editar_ProductoTienda,name='editar_ProductoTienda'),


    #añadir pieza de una tienda en el carrito 
    path('anadir-pieza-carrito/<int:productoTienda_id>/', views.anadir_producto_tienda_carrito, name='anadir_producto_tienda_carrito'),


    #búsqueda pieza
    path('buscar-pieza', views.pieza_Buscar, name='pieza_Buscar'),
    path('busqueda-avanzada-pieza', views.busqueda_avanzada_pieza, name='busqueda_avanzada_pieza'),
    
    #tabla pedidos
    path('pedidos',views.lista_pedidos,name='lista_pedidos'),
    # path('crear-pedido',views.pedido_create,name='pedido_create'),
    
    #linea de pedido
    path('detalle-linea-pedido/<int:id_pedido>',views.dame_lineaPedido,name='dame_lineaPedido'),
    path('listar-linea-pedido-carrito/<int:id_usuario>',views.listarLineaPedidoCarrito,name='listarLineaPedidoCarrito'),
    path('eliminar-linea-pedido/<int:id_lineaPedido>',views.lineaPedido_delete,name='lineaPedido_delete'),
    path('editar-linea-pedido/<int:id_lineaPedido>/', views.editar_linea_pedido, name='editar_linea_pedido'),
    
    # urls.py
    path('finalizar-pedido/<int:pedido_id>/', views.finalizar_pedido, name='finalizar_pedido'),
    
    #devolucion
    path('devolucion/<int:lineaPedido_id>/', views.devolver_pieza, name='devolver_pieza'),
    path('lista-devoluciones', views.lista_devoluciones, name='lista_devoluciones'),
    path('devolucion/aceptar/<int:id_devolucion>/', views.aceptar_devolucion, name='aceptar_devolucion'),
    path('devolucion/denegar/<int:id_devolucion>/', views.denegar_devolucion, name='denegar_devolucion'),

    #datos de la api
    path('lista-productos-terceros/', views.listar_productos_terceros_api, name='listar_productos_terceros_api'),
    path('crear-producto-tercero/', views.crear_producto_tercero, name='crear_producto_tercero'),
    path('editar-nombre-producto-tercero/<int:producto_id>', views.editar_nombre_producto_tercero, name='editar_nombre_producto_tercero'),
    path('eliminar-producto/<int:producto_id>/', views.eliminar_producto, name='eliminar_producto'),
        

    
]