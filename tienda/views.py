from django.shortcuts import redirect, render
from .models import *
from datetime import datetime
from .forms import *
from django.contrib.auth.models import Group
from django.contrib.auth import login
from django.contrib.auth.decorators import permission_required
from django.contrib import messages
from django.http import Http404
import requests


def index(request):
    if not "fecha_inicio" in request.session:
        request.session["fecha_inicio"] = datetime.now().strftime("%d/%m/%Y %H:%M")

    return render(request, "index.html", {})


@permission_required("tienda.view_cliente")
def lista_clientes(request):
    clientes = Cliente.objects.all()
    return render(request, "cliente/lista_cliente.html", {"clientes_mostrar": clientes})


@permission_required("tienda.view_vendedor")
def lista_vendedores(request):
    vendedores = Vendedor.objects.all()
    return render(
        request, "vendedor/lista_vendedores.html", {"vendedores_mostrar": vendedores}
    )


def registrar_usuario(request):
    if request.method == "POST":
        # recogemos los datos del formulario
        formulario = RegistroForm(request.POST)

        if formulario.is_valid():
            user = formulario.save()
            rol = int(formulario.cleaned_data.get("rol"))

            if rol == Usuario.CLIENTE:
                grupo = Group.objects.get(name="clientes")
                grupo.user_set.add(user)

                # se asocia el cliente con usuario
                cliente = Cliente.objects.create(usuario=user)
                cliente.save()

            elif rol == Usuario.VENDEDOR:
                grupo = Group.objects.get(name="vendedores")
                grupo.user_set.add(user)

                # se asocia el vendedor con usuario
                vendedor = Vendedor.objects.create(usuario=user)
                vendedor.save()

            login(request, user)
            return redirect("index")

    else:
        formulario = RegistroForm()
    return render(request, "registration/signup.html", {"formulario": formulario})



def lista_catalogo(request):
    pieza = Pieza.objects.all()
    return render(request, "piezas/lista_catalogo.html", {"piezas_mostrar": pieza})


@permission_required("tienda.add_pieza")
def pieza_create(request):
    if request.method == "POST":
        formulario = PiezaModelForm(request.POST)

        if formulario.is_valid():
            print("Es valido")
            formulario.save()

            messages.success(request, "Se ha añadido la pieza")

            return redirect("lista_pieza")
    else:
        formulario = PiezaModelForm()
    return render(request, "piezas/pieza_form.html", {"formulario": formulario})


def dame_producto(request, id_pieza):
    pieza = Pieza.objects.filter(id=id_pieza).first()
    return render(request, "piezas/pieza_id.html", {"pieza": pieza})


@permission_required("tienda.change_pieza")
def pieza_editar(request, id_pieza):
    pieza = Pieza.objects.get(id=id_pieza)

    if request.method == "POST":
        # request.POST: recogemos los datos del formulario escritos del usuario
        # instance: recogemos el objeto que queremos editar
        formulario = PiezaModelForm(request.POST, instance=pieza)

        # si no hay errores de las validaciones del formulario
        if formulario.is_valid():
            print("Es valido")
            formulario.save()

            messages.success(request, "Se ha editado la pieza")

            return redirect("dame_producto", id_pieza=pieza.id)
            # return redirect("lista_pieza")

    else:
        formulario = PiezaModelForm(instance=pieza)

    return render(
        request, "piezas/pieza_editar.html", {"formulario": formulario, "pieza": pieza}
    )


@permission_required("tienda.delete_tienda")
def tienda_eliminar(request, id_tienda):
    tienda = Tienda.objects.get(id=id_tienda)

    try:
        tienda.delete()
        messages.success(
            request, "Se ha eliminado la pieza " + tienda.direccion + " correctamente"
        )

        return redirect("lista_tienda")
    
    
    except Exception as error:
        print(error)
    return redirect("lista_pieza")



@permission_required("tienda.delete_pieza")
def pieza_eliminar(request, id_pieza):
    pieza = Pieza.objects.get(id=id_pieza)

    try:
        pieza.delete()
        messages.success(
            request, "Se ha elimnado la pieza " + pieza.nombre + " correctamente"
        )

    except Exception as error:
        print(error)
    return redirect("lista_pieza")


# Modelo tienda
# TODO: hacer try catch en consultas de la bd
@permission_required("tienda.view_tienda")
def lista_tienda(request):
    tienda = Tienda.objects.all()
    return render(request, "tienda/lista_tienda.html", {"tienda_mostrar": tienda})


@permission_required("tienda.add_tienda")
def tienda_create(request):
    if request.method == "POST":
        formulario = TiendaModelForm(request.POST)

        if formulario.is_valid():
            tienda = Tienda.objects.create(
                direccion=formulario.cleaned_data.get("direccion"),
                telefono=formulario.cleaned_data.get("telefono"),
                email=formulario.cleaned_data.get("email"),
                vendedor=request.user.vendedor,)
            tienda.save()
            messages.success(request, "Agregada tienda")
            return redirect("lista_tienda")
        else:
            # Si el formulario no es válido, vuelve a renderizar la página con los errores
            return render(request, "tienda/crear_tienda.html", {"formulario": formulario})

    else:
        formulario = TiendaModelForm()
        return render(request, "tienda/crear_tienda.html", {"formulario": formulario})



@permission_required("tienda.view_tienda")
def dame_tienda(request, id_tienda):
    tienda = Tienda.objects.get(id=id_tienda)
    
    productoTiendaDetalle = Producto_Tienda.objects.filter(tienda_id=tienda).first()
    return render(request, "tienda/tienda_detalle.html", {"tienda": tienda,"productoTiendaDetalle":productoTiendaDetalle})


@permission_required("tienda.change_tienda")
def tienda_editar(request, id_tienda):
    tienda = Tienda.objects.get(id=id_tienda)

    if request.method == "POST":

        formulario = TiendaModelForm(request.POST, instance=tienda)

        if formulario.is_valid():
            print("Es valido")
            formulario.save()

            messages.success(request, "Se ha editado la tienda")

            return redirect("lista_tienda")

    else:
        formulario = TiendaModelForm(instance=tienda)

    return render(
        request,
        "tienda/tienda_editar.html",
        {"formulario": formulario, "tienda": tienda},
    )  #'tienda': tienda: es cuando el formulario vacio


# modelo cliente
@permission_required("tienda.view_cliente")
def perfil_cliente(request, id_usuario):

    if request.user.cliente.id == id_usuario:
        cliente = Cliente.objects.get(id=id_usuario)
        return render(request, "cliente/perfil_cliente.html", {"cliente": cliente})
    else:
        raise Http404()


@permission_required("tienda.view_cuentabancaria")
def ver_detalle_cuentaBancaria_Cliente(request, id_usuario):
    # Obtenemos el cliente asociado al usuario
    cliente = Cliente.objects.filter(usuario_id=id_usuario).first()

    # Obtenemos la cuenta bancaria asociada al cliente
    cuentaBancariaCliente = CuentaBancaria.objects.filter(cliente=cliente).first()

    return render(
        request,
        "cliente/detalleCuentaBancariaCliente.html",
        {"cuentaBancariaCliente": cuentaBancariaCliente},
    )

@permission_required("tienda.add_cuentabancaria")
def cuentaBancaria_create(request):
    if request.method == "POST":
        formulario = CuentaBancariaModelForm(request.POST)

        if formulario.is_valid():
            cuenta = CuentaBancaria.objects.create(
                iban=formulario.cleaned_data.get("iban"),
                banco=formulario.cleaned_data.get("banco"),
                moneda=formulario.cleaned_data.get("moneda"),
                cliente=request.user.cliente,
            )
            cuenta.save()
            messages.success(request, "Agregada cuenta bancaria")
            return redirect(
                "ver_detalle_cuentaBancaria_Cliente", id_usuario=request.user.id
            )
            
        else:
            return render(request, "cliente/crear_cuentaBancaria.html", {"formulario": formulario})
    else:
        formulario = CuentaBancariaModelForm()
    return render(
        request, "cliente/crear_cuentaBancaria.html", {"formulario": formulario}
    )


# Borrar cuenta bancaria
@permission_required("tienda.delete_cuentabancaria")
def cuentaBancaria_delete(request, id_cuenta):
    cuenta = CuentaBancaria.objects.get(id=id_cuenta)

    try:
        cuenta.delete()
        messages.success(request, "Se ha eliminado la cuenta bancaria correctamente.")

    except Exception as error:
        print(error)

    return redirect("ver_detalle_cuentaBancaria_Cliente", id_usuario=cuenta.cliente.id)

@permission_required("tienda.change_cuentabancaria")
def cuentaBancaria_editar(request, id_cuentaaBancaria):
    cuentaBancariaQuery = CuentaBancaria.objects.get(id=id_cuentaaBancaria)

    if request.method == "POST":
        # request.POST: recogemos los datos del formulario escritos del usuario
        # instance: recogemos el objeto que queremos editar
        formulario = CuentaBancariaModelForm(request.POST, instance=cuentaBancariaQuery)

        # si no hay errores de las validaciones del formulario
        if formulario.is_valid():
            formulario.save()

            messages.success(request, "Se ha editado la cuenta bancaria")

            return redirect(
                "ver_detalle_cuentaBancaria_Cliente", id_usuario=request.user.id
            )

    else:
        formulario = CuentaBancariaModelForm(instance=cuentaBancariaQuery)

    return render(
        request,
        "cliente/cuentaBancaria_editar.html",
        {"formulario": formulario, "cuentaBancariaQuery": cuentaBancariaQuery},
    )


@permission_required("tienda.view_vendedor")
def perfil_vendedor(request, id_usuario):
    if request.user.vendedor.id == id_usuario:
        vendedor = Vendedor.objects.get(id=id_usuario)
        return render(request, "vendedor/perfil_vendedor.html", {"vendedor": vendedor})
    else:
        raise Http404()

@permission_required("tienda.view_vendedor")
def ver_detalle_datosVendedor(request, id_usuario):
    # Obtenemos el cliente asociado al usuario
    vendedor = Vendedor.objects.filter(usuario_id=id_usuario).first()

    # Obtenemos la cuenta bancaria asociada al cliente
    datosVendedorQuery = DatosVendedor.objects.filter(vendedor_id=vendedor).first()

    return render(
        request,
        "vendedor/detalleDatosVendedor.html",
        {"datosVendedorQuery": datosVendedorQuery},
    )


@permission_required('tienda.create_datosvendedor')
def datosVendedor_create(request):
    if request.method == "POST":
        formulario = DatosVendedorModelForm(request.POST)

        if formulario.is_valid():
            datosVendedor = DatosVendedor.objects.create(
                direccion=formulario.cleaned_data.get("direccion"),
                facturacion=formulario.cleaned_data.get("facturacion"),
                vendedor=request.user.vendedor,
            )
            datosVendedor.save()
            messages.success(request, "Agregada datos vendedor")
            return redirect("ver_detalle_datosVendedor", id_usuario=request.user.id)
    else:
        formulario = DatosVendedorModelForm()
    return render(
        request, "vendedor/crear_datosVendedor.html", {"formulario": formulario}
    )


@permission_required("tienda.delete_datosvendedor")
def datosVendedor_delete(request, id_Datovendedor):
    datosVendedorQuery = DatosVendedor.objects.filter(id=id_Datovendedor).first()

    try:
        datosVendedorQuery.delete()
        messages.success(
            request, "Se ha eliminado los datos del vendedor correctamente."
        )

    except Exception as error:
        print(error)

    return redirect(
        "ver_detalle_datosVendedor", id_usuario=datosVendedorQuery.vendedor.usuario.id
    )


@permission_required("tienda.change_datosvendedor")
def datosVendedor_editar(request, id_Datovendedor):
    datosVendedorQuery = DatosVendedor.objects.filter(id=id_Datovendedor).first()

    if request.method == "POST":
        # request.POST: recogemos los datos del formulario escritos del usuario
        # instance: recogemos el objeto que queremos editar
        formulario = DatosVendedorModelForms_Editar(request.POST, instance=datosVendedorQuery)

        # si no hay errores de las validaciones del formulario
        if formulario.is_valid():
            formulario.save()

            messages.success(request, "Se ha editado los datos del vendedor")

            return redirect(
                "ver_detalle_datosVendedor",
                id_usuario=datosVendedorQuery.vendedor.usuario.id,
            )

    else:
        formulario = DatosVendedorModelForms_Editar(instance=datosVendedorQuery)

    return render(
        request,
        "vendedor/datosVendedor_editar.html",
        {"formulario": formulario, "datosVendedorQuery": datosVendedorQuery},
    )


# pruba agregar producto para probar
@permission_required("tienda.add_producto_tienda")
def agregar_ProductoTienda(request):
    if request.method == "POST":
        formulario = DatosVendedorModelForms(request.POST, request=request)

        if formulario.is_valid():
            # aqui vemos si existe en inventario hay un producto existente
            inventario = Producto_Tienda.objects.filter(
                tienda=formulario.cleaned_data.get("tienda"),
                pieza=formulario.cleaned_data.get("pieza"),
            ).first()

            if inventario is None:
                formulario.save()

                return redirect("lista_ProductosTienda")

            else:
                inventario.cantidad += formulario.cleaned_data.get("cantidad")

                inventario.save()

                return redirect("lista_ProductosTienda")

    else:
        formulario = DatosVendedorModelForms(None, request=request)
    return render(
        request, "productosTienda/crear_productoTienda.html", {"formulario": formulario}
    )

@permission_required("tienda.view_producto_tienda")
def lista_ProductosTienda(request):
    productosTiendas = Producto_Tienda.objects.prefetch_related("tienda", "pieza").all()
    return render(
        request, "productosTienda/lista_productosTienda.html", {"productosTiendas": productosTiendas}
    )

@permission_required("tienda.change_producto_tienda")
def editar_ProductoTienda(request, id_ProductoTienda):
    productoTiendaRegistros = Producto_Tienda.objects.prefetch_related("tienda", "pieza").all()
    productoTiendaRegistrosUnico = productoTiendaRegistros.filter(id=id_ProductoTienda).first()

    if request.method == "POST":
        formulario = DatosInventarioEditarModelForms(request.POST, instance=productoTiendaRegistrosUnico)

        if formulario.is_valid():

            formulario.save()
            messages.success(request, "Editada la cantidad")

            return redirect("lista_ProductosTienda")

    else:
        formulario = DatosInventarioEditarModelForms(instance=productoTiendaRegistrosUnico)

    return render(
        request,
        "productosTienda/editar_ProductoTienda.html",
        {"formulario": formulario, "productoTiendaRegistrosUnico": productoTiendaRegistrosUnico},
    )

@permission_required("tienda.delete_producto_tienda")
def productoTienda_delete(request, id_productoTienda):
    productoTiendaRegistros = Producto_Tienda.objects.prefetch_related("tienda", "pieza").all()
    
    productoTiendaRegistrosUnico = productoTiendaRegistros.filter(id=id_productoTienda).first()

    try:
        productoTiendaRegistrosUnico.delete()
        messages.success(request, "Se ha eliminado los datos del inventario.")

        return redirect("lista_ProductosTienda")

    except Exception as error:
        print(error)


def pieza_Buscar(request):

    if request.GET:
        formulario = BusquedaPiezaModelForm(request.GET)

        if formulario.is_valid():
            pieza = Pieza.objects.all()

            # Obtenemos el nombre del formulario
            nombre = formulario.cleaned_data.get("nombre")

            # Filtramos las piezas por nombre
            piezaEncontrada = pieza.filter(nombre__icontains=nombre)

            return render(
                request,
                "piezas/resultado_Busqueda.html",
                {"piezaEncontrada": piezaEncontrada},
            )

    else:
        formulario = BusquedaPiezaModelForm()

    return render(request, "piezas/pieza_Busqueda.html", {"formulario": formulario})

@permission_required("tienda.view_pedido")
def lista_pedidos(request):
    pedidos= Pedido.objects.select_related("cliente").all()
    return render(request, "pedido/lista_pedidos.html", {"pedidos_mostrar": pedidos})
    

@permission_required("tienda.add_pedido")
def pedido_create(request):
    if request.method == "POST":
        formulario = PedidoModelForm(request.POST)

        if formulario.is_valid():
            #Creamos el pedido
            pedido = Pedido.objects.create(
                    estado='P',
                    fecha=formulario.cleaned_data.get("fecha"),
                    direccion=formulario.cleaned_data.get("direccion"),
                    cliente=request.user.cliente
                )
            
            pedido.save()

            messages.success(request, "Pedido realizado con éxito. Stock actualizado.")
            return redirect("lista_pedidos") 


    else:
        formulario = PedidoModelForm()

    return render(request, "pedido/crear_pedido.html", {"formulario": formulario})




# def comprar_inventario_view_antigua(request, productoTienda_id):
#     producto_tienda = Producto_Tienda.objects.filter(id=productoTienda_id).first()

#     if request.method == 'POST':
#         #producto_tienda: pasamos ese registro de la bd al formulario
#         #request.POST: recogemos los datos del formulario escritos del usuario
#         formulario = CompraProductoTiendaModelForm(request.POST, producto_tienda_obj=producto_tienda)
#         if formulario.is_valid():
#             cantidad = formulario.cleaned_data['cantidad']
#             direccion = formulario.cleaned_data['direccion']

#             producto_tienda.cantidad -= cantidad
#             producto_tienda.save()

#             cliente = Cliente.objects.filter(usuario=request.user).first()
#             Pedido.objects.create(
#                 cliente=cliente,
#                 pieza=producto_tienda.pieza,
#                 direccion=direccion,
#                 estado='P'
#             )

#             messages.success(request, "Compra realizada con éxito. Stock actualizado.")
#             return redirect('lista_pedidos')
#     else:
#         formulario = CompraProductoTiendaModelForm(producto_tienda_obj=producto_tienda)

#     return render(request, 'compra/formulario_compra.html', {'formulario': formulario})

    """
1- Comprobar si existe un pedido de ese cliente por si esta pendiente

2- Sino existe, lo creo

Si existe, lo actualizo


    """


# @permission_required("tienda.add_pedido")
# def comprar_producto_tienda(request, productoTienda_id):
#     producto_tienda = Producto_Tienda.objects.filter(id=productoTienda_id).first()
#     cliente = Cliente.objects.get(usuario=request.user)

#     if request.method == 'POST':
#         formulario = CompraProductoTiendaModelForm(request.POST, producto_tienda_obj=producto_tienda)
#         if formulario.is_valid():
#             stock = formulario.cleaned_data['stock']
#             direccion = formulario.cleaned_data['direccion'] #QUITAR

#             # 1. Creamos el pedido
#             pedido = Pedido.objects.create(
#                 cliente=cliente,
#                 direccion=direccion, #QUITAR O DEJARLO VACIO HASTA LA COMPRA
#                 estado='P',  # O el estado que corresponda
#             )

#             # 2. Creamos la línea de pedido asociada
#             LineaPedido.objects.create(
#                 pedido=pedido,
#                 pieza=producto_tienda.pieza,
#                 tienda=producto_tienda.tienda,
#                 precio=producto_tienda.precio,
#                 cantidad=stock, #quitar 
#             )



#             messages.success(request, "Compra realizada con éxito. Stock actualizado.")
#             return redirect('lista_pedidos')
#     else:
#         formulario = CompraProductoTiendaModelForm(producto_tienda_obj=producto_tienda)

#     return render(request, 'compra/formulario_compra.html', {'formulario': formulario, 'producto_tienda': producto_tienda})

@permission_required("tienda.add_pedido")
def anadir_producto_tienda_carrito(request, productoTienda_id):
    #obtenemos el id del productoTienda
    producto_tienda = Producto_Tienda.objects.filter(id=productoTienda_id).first()
    
    #obtenemos usuario cliente
    cliente = Cliente.objects.get(usuario=request.user)

    if request.method == 'POST':
        formulario = AnadirProductoTiendaModelForm(request.POST, producto_tienda_obj=producto_tienda)
        if formulario.is_valid():
            cantidad = formulario.cleaned_data['cantidad'] 

            # 1. Buscamos pedido pendiente
            pedido = Pedido.objects.filter(cliente=cliente, estado='P').first()
            
            if not pedido:
                # Si no existe lo creo
                pedido = Pedido.objects.create(
                    cliente=cliente,
                    direccion="",  # O pide la dirección en el formulario
                    estado='P',
                )
                pedido.save()

            # 2. Agregamos la línea de pedido (o actualizamos si ya existe la misma pieza y tienda)
            linea_existente = LineaPedido.objects.filter(
                pedido=pedido,
                pieza=producto_tienda.pieza,
                tienda=producto_tienda.tienda
            ).first()

            # Si ya existe una línea de pedido para esa pieza y tienda, actualizamos la cantidad
            if linea_existente:
                linea_existente.cantidad += cantidad
                linea_existente.save()
            else:
                LineaPedido.objects.create(
                    pedido=pedido,
                    pieza=producto_tienda.pieza,
                    tienda=producto_tienda.tienda,
                    precio=producto_tienda.precio,
                    cantidad=cantidad,
                )


            messages.success(request, "Compra realizada con éxito. Stock actualizado.")
            return redirect('lista_pedidos')
    else:
        formulario = AnadirProductoTiendaModelForm(producto_tienda_obj=producto_tienda)

    return render(request, 'carrito/formulario_agregarPiezas.html', {'formulario': formulario, 'producto_tienda': producto_tienda})


def dame_lineaPedido(request, id_pedido):
    linea_pedido = LineaPedido.objects.filter(pedido=id_pedido).all()
    
    #productoTiendaDetalle = Producto_Tienda.objects.filter(tienda_id=tienda).first()
    return render(request, "lineaPedido/lineaPedido_detalle.html", {"linea_pedido": linea_pedido})
    
from django.db.models import Q
def busqueda_avanzada_pieza(request):
    #Obtenemos todos los productos de la tienda
    QSProductoTienda = Producto_Tienda.objects.select_related("tienda", "pieza").all() 
    
    if len(request.GET) > 0:  # Si hay datos en la URL...
        formulario = BusquedaAvanzadaPiezaForm(request.GET)  # Creamos el formulario con esos datos
        
        if formulario.is_valid():  # Si los datos son correctos según el formulario...
            
            #obtenemos los filtros
            direccion = formulario.cleaned_data.get('direccion')
            precioMen = formulario.cleaned_data.get('precioMen')
            precioMay = formulario.cleaned_data.get('precioMay')
            stock = formulario.cleaned_data.get('stock')
            
            condiciones = Q()  # Crea un objeto Q vacío (inicialmente sin condiciones)
            if direccion:
                condiciones &= Q(tienda__direccion__icontains=direccion)
            if precioMen is not None:
                #gte: Mayor o igual que
                condiciones &= Q(pieza__precio__gte=precioMen) 
            if precioMay is not None:
                #lte: Menor o igual que
                condiciones &= Q(pieza__precio__lte=precioMay) 
            if stock is not None:
                condiciones &= Q(stock=stock)

            QSProductoTienda = QSProductoTienda.filter(condiciones)
            
            print(Producto_Tienda.objects.filter(pieza__precio__gte=5, pieza__precio__lte=9).values('pieza__precio'))

            
            
            return render(request, 'piezas/pieza_BusquedaAvanzada.html', {
                'formulario': formulario,
                'QSProductoTienda': QSProductoTienda})

    
    else:  # Si no hay datos en la URL
        formulario = BusquedaAvanzadaPiezaForm(None)  # Creamos un formulario vacío

    return render(request, 'piezas/pieza_BusquedaAvanzada.html', {'formulario': formulario})

    
from django.db.models import Sum, F
# def listarLineaPedidoCarrito(request, id_usuario):
#     # Filtra las líneas del pedido pendiente de ese cliente
#     lineas = LineaPedido.objects.filter(pedido__cliente_id=id_usuario, pedido__estado='P')
    
#     # Obtenemos el pedido pendiente de ese cliente (puede ser None si no hay)
#     pedido = Pedido.objects.filter(cliente_id=id_usuario, estado='P').first()

#     # Calcula la suma total de todas las cantidades y el precio total (cantidad * precio)
#     totales = lineas.aggregate( #usamos aggregate para hacer calculos con los registros del modelo
#         total_cantidad=Sum('cantidad'),
#         #F: se usa para obtener las columnas de la base de datos
#         total_precio=Sum(F('cantidad') * F('precio'))
#     )

#     # Por si no hay nada, evita que sean None
#     total_productos = totales['total_cantidad'] or 0
#     total_precio = totales['total_precio'] or 0

#     # Envía la lista y los totales al template
#     return render(request, 'lineaPedido/totalPiezascarrito.html', {
#         'carrito': lineas,
#         'total_productos': total_productos,
#         'total_precio': total_precio,
#         'pedido': pedido 
#     })
    
    
def listarLineaPedidoCarrito(request, id_usuario):
    # Filtramos las líneas del pedido pendiente de ese cliente
    lineas = LineaPedido.objects.select_related('pedido', 'pieza', 'tienda').filter(
        pedido__cliente_id=id_usuario,
        pedido__estado='P'
    )

    # Obtenemos el pedido pendiente de ese cliente 
    pedido = Pedido.objects.filter(cliente_id=id_usuario, estado='P').first()

    #Calculamos la suma total de todas las cantidades y el precio total (cantidad * precio)
    totales = lineas.aggregate(
        total_cantidad=Sum('cantidad'),
        total_precio=Sum(F('cantidad') * F('precio'))
    )

    #Por si no hay nada, evita que sean None
    total_productos = totales['total_cantidad'] or 0
    total_precio = totales['total_precio'] or 0

    # Envía la lista, los totales y el pedido al template
    return render(request, 'lineaPedido/totalPiezascarrito.html', {
        'carrito': lineas,
        'total_productos': total_productos,
        'total_precio': total_precio,
        'pedido': pedido,
    })

   

def lineaPedido_delete(request, id_lineaPedido):
    #Hacemos la consulta la linea de pedido
    lineaPedido = LineaPedido.objects.filter(id=id_lineaPedido).first()
    
    try:
        lineaPedido.delete()
        messages.success(request, "Se ha eliminado la pieza del carrito correctamente.")
    except Exception as error:
        print(error)
    
    return redirect("listarLineaPedidoCarrito", id_usuario=request.user.cliente.id)



#editar_linea_pedido
def editar_linea_pedido(request, id_lineaPedido):
    linea = LineaPedido.objects.filter(id=id_lineaPedido).first()
    
    if request.method == 'POST':
        formulario = EditarLineaPedidoForm(request.POST, instance=linea)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Cantidad actualizada correctamente.")
            return redirect("listarLineaPedidoCarrito", id_usuario=request.user.cliente.id)
    else:
        formulario = EditarLineaPedidoForm(instance=linea)

    return render(request, 'carrito/editar_linea.html', {'formulario': formulario, 'linea': linea})



def finalizar_pedido(request, pedido_id):
    pedido = Pedido.objects.filter(id=pedido_id, estado='P').first()
    
    if request.method == 'POST':
        formulario = FinalizarPedidoForm(request.POST, instance=pedido)
        if formulario.is_valid():
            #Actualizamos dirección y estado
            pedido.direccion = formulario.cleaned_data['direccion']
            pedido.estado = 'C'
            pedido.save()
            
            messages.success(request, "Tu compra se ha realizado con éxito.")
            return redirect("lista_pedidos")
            
            
    else:
        formulario = FinalizarPedidoForm(instance=pedido)
        
    return render(request, 'carrito/finalizar_pedido.html', {'formulario': formulario, 'pedido': pedido})


def listar_productos_terceros_api(request):
    
    if request.user.is_anonymous:
        return mi_error_500(request)

    if request.user.rol != 3:
        #llamamos a mi metodo de error 500
        return mi_error_500(request)
        
    
    headers= {
        'Authorization': 'Bearer dulmwogNLx4iwVhfpZBTXR1RtTkq3g'
    }
    
    #datos de la API
    response = requests.get('http://0.0.0.0:8081/api/v1/listar_productosTercero/',
                            headers=headers)
    
    #transformar los datos a un formato JSON
    listar_productosTercero_Api = response.json()
    
    return render(request, "productos_terceros_api/productosTerceros.html", {"productos": listar_productosTercero_Api})


def crear_producto_tercero(request):
    if request.user.is_anonymous:
        return mi_error_500(request)

    if request.user.rol != 3:
        #llamamos a mi metodo de error 500
        return mi_error_500(request)

    #enviamos a la vista del formulario para crear un producto tercero
    if request.method == "POST":
        formulario = CrearProductoTerceroForm(request.POST)

        if formulario.is_valid():
            # Enviamos los datos a la API
            headers = {
                'Authorization': 'Bearer dulmwogNLx4iwVhfpZBTXR1RtTkq3g',
                #'Content-Type': 'application/json'
            }
            
            
            
            response = requests.post('http://0.0.0.0:8081/api/v1/crear-producto-tercero/',
                            headers=headers,
                            data=formulario.cleaned_data)
            
            
    
            #transformar los datos a un formato JSON
            respuesta_api= response.json()
            
            messages.success(request, "Producto creado correctamente.")
            
            return redirect("listar_productos_terceros_api")
    else:
        formulario = CrearProductoTerceroForm()
        return render(request, "productos_terceros_api/crear_productoTercero.html", {"formulario": formulario})



# Pagina de error
def mi_error_404(request, exception=None):
    return render(request, "errores/404.html", None, None, 404)


def mi_error_500(request, exception=None):
    return render(request, "errores/500.html", None, None, 404)
