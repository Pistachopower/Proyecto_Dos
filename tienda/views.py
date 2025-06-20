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
from django.contrib.auth.decorators import login_required


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
@permission_required("tienda.view_cuentabancaria")
def perfil_cliente(request, id_usuario):

    if request.user.cliente.id == id_usuario:
        cliente = Cliente.objects.get(id=id_usuario)
        return render(request, "cliente/perfil_cliente.html", {"cliente": cliente})
    else:
        mi_error_500(request)


@permission_required("tienda.view_cuentabancaria")
def ver_detalle_cuentaBancaria_Cliente(request, id_usuario):
    
    # Verificamos que el usuario autenticado esté viendo solo su propia cuenta
    if request.user.id != int(id_usuario):
        #raise PermissionDenied("No tienes permiso para ver esta cuenta bancaria.")
        mi_error_500(request)
        
    else:
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
        mi_error_500(request)
        return redirect("index")

@permission_required("tienda.view_vendedor")
def ver_detalle_datosVendedor(request, id_usuario):
        # Comparamos el usuario del vendedor con el id_usuario recibido
    if request.user.vendedor.usuario.id == id_usuario:
        # Obtenemos el cliente asociado al usuario
        vendedor = Vendedor.objects.filter(usuario_id=id_usuario).first()

        # Obtenemos la cuenta bancaria asociada al cliente
        datosVendedorQuery = DatosVendedor.objects.filter(vendedor_id=vendedor).first()

        return render(
            request,
            "vendedor/detalleDatosVendedor.html",
            {"datosVendedorQuery": datosVendedorQuery},)
    else:
        mi_error_500(request)
        return redirect("index")


@permission_required('tienda.add_datosvendedor')
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


@permission_required("tienda.add_producto_tienda")
def agregar_ProductoTienda(request):
    if request.method == "POST":
        formulario = DatosVendedorModelForms(request.POST, request=request)

        if formulario.is_valid():
            # Aquí vemos si existe en inventario hay un producto existente
            inventario = Producto_Tienda.objects.filter(
                tienda=formulario.cleaned_data.get("tienda"),
                pieza=formulario.cleaned_data.get("pieza"),
            ).first()

            if inventario is None:
                formulario.save()

                return redirect("lista_ProductosTienda")

            else:
                inventario.stock += formulario.cleaned_data.get("stock")

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

@login_required
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
    #obtenemos el vendedor
    vendedor= Vendedor.objects.filter(usuario= request.user).first()
    
    #luego obtenemos las tiendas que le pertenecen al vendedor
    tiendasVendedor= Tienda.objects.filter(vendedor=vendedor).all()
    
    pedidos= []
    
    #Comprobamos el rol del usuario accediendo al enumerado de Usuario
    if request.user.rol == Usuario.VENDEDOR:
        
        #muestra los pedidos de la tienda del vendedor
        pedidos = Pedido.objects.select_related("cliente", "tienda").filter(tienda__in=tiendasVendedor)

        
    if request.user.rol == Usuario.CLIENTE:
        #obtenemos solo los pedidos del usuario activo
        cliente= Cliente.objects.filter(usuario= request.user).first()
        
        pedidos= Pedido.objects.select_related("cliente").filter(cliente=cliente)
        
    
    return render(request, "pedido/lista_pedidos.html", {"pedidos_mostrar": pedidos})
    
    
    

# @permission_required("tienda.add_pedido")
# def pedido_create(request):
#     if request.method == "POST":
#         formulario = PedidoModelForm(request.POST)

#         if formulario.is_valid():
#             #Creamos el pedido
#             pedido = Pedido.objects.create(
#                     estado='P',
#                     fecha=formulario.cleaned_data.get("fecha"),
#                     direccion=formulario.cleaned_data.get("direccion"),
#                     cliente=request.user.cliente
#                 )
            
#             pedido.save()

#             messages.success(request, "Pedido realizado con éxito. Stock actualizado.")
#             return redirect("lista_pedidos") 


#     else:
#         formulario = PedidoModelForm()

#     return render(request, "pedido/crear_pedido.html", {"formulario": formulario})




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
                    tienda = producto_tienda.tienda, #agregamos el pedido con la tienda
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


            messages.success(request, "Producto añadido al carrito con éxito.")
            return redirect('listarLineaPedidoCarrito', id_usuario=request.user.cliente.id)
    else:
        formulario = AnadirProductoTiendaModelForm(producto_tienda_obj=producto_tienda)

    return render(request, 'carrito/formulario_agregarPiezas.html', {'formulario': formulario, 'producto_tienda': producto_tienda})

@permission_required("tienda.view_lineapedido")
def dame_lineaPedido(request, id_pedido):
    # 1. Obtenemos los registros que coincidan con el id_pedido
    linea_pedido = LineaPedido.objects.filter(pedido=id_pedido).all()
    
    #2- Creamos una lista donde guardaremos todas las devoluciones de las piezas más un nuevo campo
    #booleano que me va a indicar si hay una devolución por cada linea pedido 
    pieza_devoluciones= []
    
    
    #Iteramos sobre cada línea de pedido p
    for linea in linea_pedido:
        # Verificamos si hay una devolución para esa línea de pedido
        devuelto= Devolucion.objects.filter(lineaPedido=linea).exists()
        
        #Agregamos un diccionario con la clave y el valor ya sea sea True o False en devuelto
        pieza_devoluciones.append({
            "linea_pedido": linea,
            "devuelto": devuelto #esta clave indica si hay una devolución para esa línea de pedido
        })

        
     # 2. Obtenemos la cuenta bancaria directamente usando relaciones
    cuenta_bancaria = CuentaBancaria.objects.filter(
        cliente__pedidos__id=id_pedido
    ).first()
    
     # 3. Calculamos el total gastado (suma de cantidad * precio)
    total = linea_pedido.aggregate(
        total_gastado=Sum(F('cantidad') * F('precio'))
    )['total_gastado'] or 0
    
    
    return render(request, "lineaPedido/lineaPedido_detalle.html", { 
                "cuenta_bancaria": cuenta_bancaria, 
                "total": total,
                "pieza_devoluciones": pieza_devoluciones}
                  )


from django.db.models import Q
@login_required
def busqueda_avanzada_pieza(request):
    #Obtenemos todos los productos de la tienda
    QSProductoTienda = Producto_Tienda.objects.select_related("tienda", "pieza").all() 
    
    if len(request.GET) > 0:  # Si hay datos en la URL...
        formulario = BusquedaAvanzadaPiezaForm(request.GET)  # Creamos el formulario con esos datos
        
        if formulario.is_valid():  # Si los datos son correctos según el formulario...
            
            #Obtenemos los filtros
            direccion = formulario.cleaned_data.get('direccion')
            precioMen = formulario.cleaned_data.get('precioMen')
            precioMay = formulario.cleaned_data.get('precioMay')
            stock = formulario.cleaned_data.get('stock')
            
            #Usamos Q para combinar operadores lógicos 
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

            #filtramos si hay alguna tienda con dichos filtros
            QSProductoTienda = QSProductoTienda.filter(condiciones)

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

@permission_required("tienda.view_lineapedido")
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
        #F: obtiene el campo de la bd  
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

   
@permission_required("tienda.delete_lineapedido")
def lineaPedido_delete(request, id_lineaPedido):
    #Hacemos la consulta la linea de pedido
    lineaPedido = LineaPedido.objects.filter(id=id_lineaPedido).first()
    
    try:
        lineaPedido.delete()
        messages.success(request, "Se ha eliminado la pieza del carrito correctamente.")
    except Exception as error:
        print(error)
    
    return redirect("listarLineaPedidoCarrito", id_usuario=request.user.cliente.id)



@permission_required("tienda.change_lineapedido")
def editar_linea_pedido(request, id_lineaPedido):
    # Buscamos la línea de pedido por su ID
    linea = LineaPedido.objects.filter(id=id_lineaPedido).first()
    if not linea:
        # Si no existe, mostramos error
        return mi_error_500(request)

    try:
        # Comprobamos que el usuario autenticado es el dueño de la línea de pedido
        if linea.pedido.cliente.usuario.id == request.user.id:
            if request.method == 'POST':
                # Si es POST, procesamos el formulario con los datos enviados
                formulario = EditarLineaPedidoForm(request.POST, instance=linea)
                if formulario.is_valid():
                    # Si el formulario es válido, guardamos los cambios
                    formulario.save()
                    messages.success(request, "Cantidad actualizada correctamente.")
                    # Redirigimos al carrito del usuario
                    return redirect("listarLineaPedidoCarrito", id_usuario=request.user.cliente.id)
            else:
                # Si es GET, mostramos el formulario con los datos actuales
                formulario = EditarLineaPedidoForm(instance=linea)

            # Renderizamos la plantilla con el formulario y la línea de pedido
            return render(request, 'carrito/editar_linea.html', {'formulario': formulario, 'linea': linea})
        else:
            # Si el usuario no es el dueño, mostramos error
            return mi_error_500(request)
    except AttributeError:
        # Si el usuario no tiene cliente asociado, mostramos error
        return mi_error_500(request)


@permission_required("tienda.view_pedido")
def finalizar_pedido(request, pedido_id):
    pedido = Pedido.objects.filter(id=pedido_id).first()
    
    if request.method == 'POST':
        #Se llena el formulario con la dirección del usuario y el pedido existente
        formulario = FinalizarPedidoForm(request.POST, instance=pedido)
        
        if formulario.is_valid():
            #Verificamos si el cliente tiene una cuenta bancaria ANTES de continuar
            cuenta = CuentaBancaria.objects.filter(cliente=pedido.cliente).first()
            if not cuenta:
                messages.error(request, "Debe registrar una cuenta bancaria antes de finalizar el pedido.")
                return render(request, 'carrito/finalizar_pedido.html', {
                            'formulario': formulario,
                            'pedido': pedido
                        })
            

            #Actualizamos dirección y estado
            pedido.direccion = formulario.cleaned_data['direccion']
            pedido.estado = 'C'
            pedido.save()
            
            # Restamos stock (ya validado en el formulario)
            for linea in pedido.pedido_lineaPedido.all():
                producto = Producto_Tienda.objects.get(tienda=linea.tienda, pieza=linea.pieza)
                producto.stock -= linea.cantidad
                producto.save()
                
            #Calculamos monto total del pedido
            total = 0  # empieza en cero
            
            for linea in pedido.pedido_lineaPedido.all():
                subtotal = linea.precio * linea.cantidad
                total += subtotal  # lo vamos sumando


            # Creamos el objeto Pago
            Pago.objects.create(
                pedido=pedido,
                cuenta_bancaria=cuenta,
                monto=total
            )
            
            
            messages.success(request, "Tu compra se ha realizado con éxito.")
            return redirect("lista_pedidos")
              
    else:
        formulario = FinalizarPedidoForm(instance=pedido)
        
    return render(request, 'carrito/finalizar_pedido.html', {'formulario': formulario, 'pedido': pedido})





@login_required
def listar_productos_terceros_api(request):
    if request.user.rol != 3:
        #llamamos a mi metodo de error 500
        return mi_error_500(request)
        
    
    headers= {
        'Authorization': 'Bearer y10KqCW7ajqPQQXpTYH39zzR3a0ff3',
        'Content-Type': 'application/json'
    }
    
    #datos de la API
    response = requests.get('http://0.0.0.0:8081/api/v1/listar_productosTercero/',
                            headers=headers)
    
    #transformar los datos a un formato JSON
    listar_productosTercero_Api = response.json()
    
    return render(request, "productos_terceros_api/productosTerceros.html", {"productos": listar_productosTercero_Api})

@login_required
def crear_producto_tercero(request):
    if request.user.rol != 3:
        #llamamos a mi metodo de error 500
        return mi_error_500(request)

    #enviamos a la vista del formulario para crear un producto tercero
    if request.method == "POST":
        formulario = CrearProductoTerceroForm(request.POST)
        
        #agregar el id del vendedor con request.user.id

        if formulario.is_valid():
            # Enviamos los datos a la API
            headers = {
                'Authorization': 'Bearer y10KqCW7ajqPQQXpTYH39zzR3a0ff3',
                'Content-Type': 'application/json'
            }
            
            #Hacemos una copia del formulario para agregar el id del usuario
            datos = formulario.cleaned_data.copy()  
            
            #Debe coincidir con el campo de la base de datos de la api
            datos['vendedor'] = request.user.id 

            
            response = requests.post('http://0.0.0.0:8081/api/v1/crear-producto-tercero/',
                            headers=headers,
                            data=json.dumps(datos)
                            ) #convertimos los datos a JSON
            
            
            
            
            # Comprobamos si la respuesta de la API es exitosa
            if(response.status_code == requests.codes.ok):
                #transformar los datos a un formato JSON
                respuesta_api= response.json()

                messages.success(request, "Producto creado correctamente.")

                return redirect("listar_productos_terceros_api")
            
            else:
                print(response.status_code)
                errores_api = response.json()
                
                #pasamos los errores de la API al formulario
                for error in errores_api:
                    formulario.add_error(error, errores_api[error])
                return render(request, "productos_terceros_api/crear_productoTercero.html", {"formulario": formulario, "errores_api": errores_api})
                
                
    else:
        formulario = CrearProductoTerceroForm()
        return render(request, "productos_terceros_api/crear_productoTercero.html", {"formulario": formulario})


import json
from requests.exceptions import HTTPError
@login_required
def editar_nombre_producto_tercero(request, producto_id):
    if request.user.rol != 3:
        #llamamos a mi metodo de error 500
        return mi_error_500(request)
    
    #Inicializamos datosFormulario como None cuando sea get,
    #es decir, cuando se entra por primera vez y tomamos
    #el registro del producto que viene de la api
    datosFormulario = None
    
    #Si entra aqui es porque el usuario ha mandado datos 
    if request.method == "POST":
        datosFormulario = request.POST
        
    producto= helper.obtener_producto(producto_id)
    
    formulario= NombreProductoForm(
        datosFormulario,
        initial={
            'nombre': producto['nombre'],
        }
    )
    
    #Enviamos los datos a la API para editar el nombre del producto
    if (request.method == "POST"):
        try:
            formulario = NombreProductoForm(request.POST)

            headers= {
                        'Authorization': 'Bearer y10KqCW7ajqPQQXpTYH39zzR3a0ff3',
                        'Content-Type': 'application/json'
                    }

            if formulario.is_valid():
                #Hacemos una copia del formulario para agregar el id del usuario
                datos = formulario.cleaned_data.copy()  

                #Debe coincidir con el campo de la base de datos de la api
                datos['vendedor'] = request.user.id 

                response = requests.patch(
                        'http://0.0.0.0:8081/api/v1/editar-nombre-producto-tercero/'+str(producto_id) + '/',
                        headers=headers,
                        data=json.dumps(datos) #convertimos los datos a JSON
                    )

                if(response.status_code == requests.codes.ok):
                        messages.success(request, "Se ha editado correctamente el nombre del producto.")
                        return redirect("listar_productos_terceros_api")

                else:
                        response.raise_for_status()
        
        except HTTPError as http_err:
            #Si hay errores en la api, los mostramos en el formulario
            if response.status_code == 400:
                errores = response.json()
                for error in errores:
                    formulario.add_error(error, errores[error])
                return render(request, 
                              'productos_terceros_api/actualizar_nombre.html',
                              {"formulario":formulario,
                               "producto":producto})

            else:
                return mi_error_500(request)
        except Exception as err:
            print(f"Ocurrió un error: {err}")
            return mi_error_500(request)
        
            
            
    return render(request, 'productos_terceros_api/actualizar_nombre.html',{"formulario":formulario,"producto":producto})
   
        
@login_required   
def eliminar_producto(request, producto_id):
    try:
        headers= {
                        'Authorization': 'Bearer y10KqCW7ajqPQQXpTYH39zzR3a0ff3',
                        'Content-Type': 'application/json'
                    }
        
        print("Usuario logueado:", request.user.username, "ID:", request.user.id)
        
        response = requests.delete(
            'http://0.0.0.0:8081/api/v1/eliminar-producto/'+str(producto_id) + '/',
            headers=headers,
        )
        if response.status_code == requests.codes.ok:
            messages.success(request, "Producto eliminado correctamente.")
            return redirect("listar_productos_terceros_api")
        elif response.status_code == 403:
            # Captura el mensaje de la API y lo muestra como error
            error_api = response.json().get("error", "No puedes eliminar el producto.")
            messages.error(request, error_api)
            return redirect("listar_productos_terceros_api")
        
        else:
            print(response.status_code)
            response.raise_for_status()
            
    except Exception as err:
        print(f"Ocurrió un error: {err}")
        return mi_error_500(request)
    return redirect("listar_productos_terceros_api")  

@login_required  
def devolver_pieza(request, lineaPedido_id):
    obtener_lineaPedido = LineaPedido.objects.filter(id=lineaPedido_id).first()
    
    #creamos el objeto devolucion
    devolucion= Devolucion.objects.create(
                lineaPedido= obtener_lineaPedido,
                cliente= obtener_lineaPedido.pedido.cliente,)
    
    
    devolucion.save()
    messages.success(request, "Se ha procesado tu devolución la pieza correctamente.")
    return redirect("dame_lineaPedido", id_pedido=obtener_lineaPedido.pedido.id)
    
@login_required     
def lista_devoluciones(request):
    #usamos una relación inversa 
    devoluciones = Devolucion.objects.filter(lineaPedido__tienda__vendedor__usuario=request.user)
    return render(request, "devoluciones/lista_devoluciones.html", {"devoluciones": devoluciones})

@login_required  
def aceptar_devolucion(request, id_devolucion):
    
    devolucion= Devolucion.objects.filter(id=id_devolucion).first()
    
    cliente= Cliente.objects.filter(usuario= devolucion.cliente.usuario).first()
    
    cliente.puntos= devolucion.lineaPedido.precio
    
    producto= Producto_Tienda.objects.filter(pieza= devolucion.lineaPedido.pieza).first()
    
    #devolvemos las piezas al stock 
    producto.stock= producto.stock + devolucion.lineaPedido.cantidad
    
    producto.save()
    
    cliente.save()
    
    devolucion.estado= "R"
    
    devolucion.save()
    
    return redirect("lista_devoluciones")
  
@login_required    
def denegar_devolucion(request, id_devolucion):
    devolucion= Devolucion.objects.filter(id=id_devolucion).first()
    
    devolucion.estado= "D"
    
    devolucion.save()
    
    return redirect("lista_devoluciones")


# Pagina de error
def mi_error_404(request, exception=None):
    return render(request, "errores/404.html", None, None, 404)


def mi_error_500(request, exception=None):
    return render(request, "errores/500.html", None, None, 404)
