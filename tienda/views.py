from django.shortcuts import redirect, render
from .models import *
from datetime import datetime
from .forms import *
from django.contrib.auth.models import Group
from django.contrib.auth import login
from django.contrib.auth.decorators import permission_required
from django.contrib import messages
from django.http import Http404


def index(request):
    if(not "fecha_inicio" in request.session):
        request.session["fecha_inicio"] = datetime.now().strftime('%d/%m/%Y %H:%M')
        
    return render(request, 'index.html',{})


@permission_required('tienda.view_cliente')
def lista_clientes(request):
    clientes= Cliente.objects.all() 
    return render(request, 'cliente/lista_cliente.html',{'clientes_mostrar':clientes})

@permission_required('tienda.view_vendedor')
def lista_vendedores(request):
    vendedores= Vendedor.objects.all() 
    return render(request, 'vendedores/lista_vendedores.html',{'vendedores_mostrar':vendedores})


def registrar_usuario(request):
    if request.method == 'POST':
        #recogemos los datos del formulario
        formulario= RegistroForm(request.POST)
        
        if formulario.is_valid():
            user= formulario.save()
            rol= int(formulario.cleaned_data.get('rol'))
            
            if (rol == Usuario.CLIENTE):
                grupo= Group.objects.get(name='clientes')
                grupo.user_set.add(user)
                
                #se asocia el cliente con usuario
                cliente= Cliente.objects.create(usuario=user)
                cliente.save()
                
            elif (rol == Usuario.VENDEDOR):
                grupo= Group.objects.get(name='vendedores')
                grupo.user_set.add(user)
                
                #se asocia el vendedor con usuario
                vendedor= Vendedor.objects.create(usuario=user)
                vendedor.save()
                
            login(request, user)
            return redirect('index')

    else:    
        formulario= RegistroForm()
    return render(request, 'registration/signup.html',{'formulario':formulario})


@permission_required('tienda.view_pieza')
def lista_pieza(request):
    pieza= Pieza.objects.all() 
    return render(request, 'piezas/lista_pieza.html',{'piezas_mostrar':pieza})


@permission_required('tienda.add_pieza')
def pieza_create(request):
    if request.method == "POST":
        formulario= PiezaModelForm(request.POST)
        
        if formulario.is_valid():
            print("Es valido")
            formulario.save()
            
            messages.success(request, "Se ha editado la pieza")
              
            return redirect("lista_pieza")
    else:
        formulario= PiezaModelForm()
    return render(request, 'piezas/pieza_form.html',{'formulario':formulario})




def dame_producto(request, id_pieza):
    pieza= Pieza.objects.get(id=id_pieza)
    
    return render(request, 'piezas/pieza_id.html',{'pieza':pieza})

@permission_required('tienda.change_pieza')
def pieza_editar(request, id_pieza):
    pieza= Pieza.objects.get(id=id_pieza)
    
    if request.method == "POST":
        #request.POST: recogemos los datos del formulario escritos del usuario
        #instance: recogemos el objeto que queremos editar
        formulario= PiezaModelForm(request.POST, instance=pieza)
        
        #si no hay errores de las validaciones del formulario
        if formulario.is_valid():
            print("Es valido")
            formulario.save()
            
            messages.success(request, "Se ha editado la pieza")
            
            return redirect("dame_producto", id= pieza.id )
            #return redirect("lista_pieza")
        

    else:
        formulario= PiezaModelForm(instance=pieza)
        
    return render(request, 'piezas/pieza_editar.html',{'formulario':formulario, 'pieza': pieza })


@permission_required('tienda.delete_pieza')
def pieza_eliminar(request, id_pieza):
    pieza= Pieza.objects.get(id= id_pieza)
    
    try:
        pieza.delete()
        messages.success(request, "Se ha elimnado la pieza "+ pieza.nombre+" correctamente")

    except Exception as error:
        print(error)
    return redirect('lista_pieza')

#Modelo tienda
#TODO: hacer try catch en consultas de la bd
@permission_required('tienda.view_tienda')
def lista_tienda(request):
    tienda= Tienda.objects.all() 
    return render(request, 'tienda/lista_tienda.html',{'tienda_mostrar':tienda})



# @permission_required('tienda.add_tienda')
# def tienda_create(request):
    
#     if request.method == "POST":
#         formulario= TiendaModelForm(request.POST)
        
#         if formulario.is_valid():
#             print("Es valido")
#             formulario.save()
#             messages.success(request, "Se ha creado la tienda")
#             return redirect("lista_tienda")
#     else:
#         formulario= TiendaModelForm()
#     return render(request, 'tienda/tienda_form.html',{'formulario':formulario})


#     if request.method == "POST":
#         formulario= TiendaModelForm(request.POST)
        
#         if formulario.is_valid():
#             print("Es valido")
#             formulario.save()
#             messages.success(request, "Se ha creado la tienda")
#             return redirect("lista_tienda")
#     else:
#         formulario= TiendaModelForm()
#     return render(request, 'tienda/tienda_form.html',{'formulario':formulario})



@permission_required('tienda.add_tienda')
def tienda_create(request):    
    if request.method == "POST":
        formulario= TiendaModelForm(request.POST)
        
        if formulario.is_valid():
            tienda = Tienda.objects.create(
                direccion = formulario.cleaned_data.get("direccion"),
                telefono = formulario.cleaned_data.get("telefono"),
                email = formulario.cleaned_data.get("email"),
                vendedor = request.user.vendedor,  
        )
        tienda.save()
        messages.success(request, 'Agregada tienda') 
        return redirect("lista_tienda" )
        
    else:
        formulario= TiendaModelForm()
        return render(request, 'tienda/crear_tienda.html', {'formulario': formulario})
        


@permission_required('tienda.view_tienda')
def dame_tienda(request, id_tienda):
    tienda= Tienda.objects.get(id=id_tienda)
    
    return render(request, 'tienda/tienda_detalle.html',{'tienda':tienda})

@permission_required('tienda.change_tienda')
def tienda_editar(request, id_tienda):
    tienda= Tienda.objects.get(id=id_tienda)
    
    if request.method == "POST":
        
        formulario= TiendaModelForm(request.POST, instance=tienda)
        
        if formulario.is_valid():
            print("Es valido")
            formulario.save()
            
            messages.success(request, "Se ha editado la tienda")
            

            return redirect("lista_tienda" )

        

    else:
        formulario= TiendaModelForm(instance=tienda)
        
    return render(request, 'tienda/tienda_editar.html',{'formulario':formulario, 'tienda': tienda }) #'tienda': tienda: es cuando el formulario vacio
    
    
    
#modelo cliente
def perfil_cliente(request, id_usuario):
#agregar    

   if request.user.cliente.id == id_usuario:
       cliente = Cliente.objects.get(id = id_usuario)
       return render(request, 'cliente/perfil_cliente.html',{'cliente':cliente})
   else:
       raise Http404()
   
   
@permission_required('tienda.view_cuentabancaria')
def ver_detalle_cuentaBancaria_Cliente(request, id_usuario):
     # Obtenemos el cliente asociado al usuario
    cliente = Cliente.objects.filter(usuario_id=id_usuario).first()
        
    # Obtenemos la cuenta bancaria asociada al cliente
    cuentaBancariaCliente = CuentaBancaria.objects.filter(cliente=cliente).first()
    
    return render (request, 'cliente/detalleCuentaBancariaCliente.html', {'cuentaBancariaCliente' : cuentaBancariaCliente})



def cuentaBancaria_create(request):
    if request.method == "POST":
        formulario= CuentaBancariaModelForm(request.POST)
        
        if formulario.is_valid():
            cuenta = CuentaBancaria.objects.create(
                iban = formulario.cleaned_data.get("iban"),
                banco = formulario.cleaned_data.get("banco"),
                moneda = formulario.cleaned_data.get("moneda"),
                cliente = request.user.cliente,  
            )
            cuenta.save()
            messages.success(request, 'Agregada cuenta bancaria') 
            return redirect ("ver_detalle_cuentaBancaria_Cliente", id_usuario=request.user.id)
    else:
        formulario= CuentaBancariaModelForm()
    return render(request, 'cliente/crear_cuentaBancaria.html', {'formulario': formulario})


#Borrar cuenta bancaria
@permission_required('tienda.delete_cuentabancaria')
def cuentaBancaria_delete(request, id_cuenta):
    cuenta = CuentaBancaria.objects.get(id=id_cuenta)

    try:
        cuenta.delete()  
        messages.success(request, "Se ha eliminado la cuenta bancaria correctamente.")
        
    except Exception as error:
        print(error)

    return redirect('ver_detalle_cuentaBancaria_Cliente', id_usuario=cuenta.cliente.id) 
        
    

def cuentaBancaria_editar(request, id_cuentaaBancaria):
    cuentaBancariaQuery= CuentaBancaria.objects.get(id=id_cuentaaBancaria)
   
    if request.method == "POST":
         #request.POST: recogemos los datos del formulario escritos del usuario
         #instance: recogemos el objeto que queremos editar
        formulario= CuentaBancariaModelForm(request.POST, instance=cuentaBancariaQuery)
       
         #si no hay errores de las validaciones del formulario
        if formulario.is_valid():
            formulario.save()
        
            messages.success(request, "Se ha editado la cuenta bancaria")
           
            return redirect("ver_detalle_cuentaBancaria_Cliente", id_usuario=request.user.id )
           
       
    else:
        formulario= CuentaBancariaModelForm(instance=cuentaBancariaQuery)
       
    return render(request, 'cliente/cuentaBancaria_editar.html',{'formulario':formulario, 'cuentaBancariaQuery': cuentaBancariaQuery })



#modelo DatosVendedor
def perfil_vendedor(request, id_usuario):
    if request.user.vendedor.id == id_usuario:
       vendedor = Vendedor.objects.get(id = id_usuario)
       return render(request, 'vendedor/perfil_vendedor.html',{'vendedor':vendedor})
    else:
       raise Http404()
   
   
def ver_detalle_datosVendedor(request, id_usuario):
     # Obtenemos el cliente asociado al usuario
    vendedor = Vendedor.objects.filter(usuario_id=id_usuario).first()
        
    # Obtenemos la cuenta bancaria asociada al cliente
    datosVendedorQuery = DatosVendedor.objects.filter(vendedor_id=vendedor).first()
    
    return render (request, 'vendedor/detalleDatosVendedor.html', {'datosVendedorQuery' : datosVendedorQuery})



#@permission_required('tienda.create_datosvendedor')
def datosVendedor_create(request):
    if request.method == "POST":
        formulario= DatosVendedorModelForm(request.POST)
        
        
        if formulario.is_valid():
            datosVendedor = DatosVendedor.objects.create(
                direccion = formulario.cleaned_data.get("direccion"),
                facturacion = formulario.cleaned_data.get("facturacion"),
                vendedor = request.user.vendedor,  
            )
            datosVendedor.save()
            messages.success(request, 'Agregada datos vendedor') 
            return redirect ("ver_detalle_datosVendedor", id_usuario=request.user.id)
    else:
        formulario= DatosVendedorModelForm()
    return render(request, 'vendedor/crear_datosVendedor.html', {'formulario': formulario})

@permission_required('tienda.delete_datosvendedor')
def datosVendedor_delete(request, id_Datovendedor):
    datosVendedorQuery = DatosVendedor.objects.filter(id=id_Datovendedor).first()

    try:
        datosVendedorQuery.delete()  
        messages.success(request, "Se ha eliminado los datos del vendedor correctamente.")
        
    except Exception as error:
        print(error)

    return redirect('ver_detalle_datosVendedor', id_usuario=datosVendedorQuery.vendedor.usuario.id)


def datosVendedor_editar(request, id_Datovendedor):
    datosVendedorQuery= DatosVendedor.objects.filter(id=id_Datovendedor).first()
   
    if request.method == "POST":
         #request.POST: recogemos los datos del formulario escritos del usuario
         #instance: recogemos el objeto que queremos editar
        formulario= DatosVendedorModelForms(request.POST, instance=datosVendedorQuery)
       
         #si no hay errores de las validaciones del formulario
        if formulario.is_valid():
            formulario.save()
        
            messages.success(request, "Se ha editado los datos del vendedor")
           
            return redirect("ver_detalle_datosVendedor", id_usuario=datosVendedorQuery.vendedor.usuario.id)
           
       
    else:
        formulario= DatosVendedorModelForms(instance=datosVendedorQuery)
       
    return render(request, 'vendedor/datosVendedor_editar.html',{'formulario':formulario, 'datosVendedorQuery': datosVendedorQuery })

#pruba agregar producto para probar
@permission_required('tienda.add_inventario')
def agregar_Inventario(request):
    if request.method == "POST":
        formulario= DatosVendedorModelForms(request.POST, request= request)
        
        
        if formulario.is_valid():
            #aqui vemos si existe en inventario hay un producto existente
            inventario= Inventario.objects.filter(tienda= formulario.cleaned_data.get("tienda"),
                                                  pieza= formulario.cleaned_data.get("pieza")).first()
            
            
            if (inventario is None):
                formulario.save()
                
                return redirect ("lista_ProductosTienda")
                
                
            else:
                inventario.cantidad+= formulario.cleaned_data.get("cantidad")
                
                inventario.save() 
                
                return redirect ("lista_ProductosTienda")
            
        
            
    else:
        formulario= DatosVendedorModelForms(None, request= request)
    return render(request, 'inventario/crear_inventario.html', {'formulario': formulario})


def lista_ProductosTienda(request):
    inventario= Inventario.objects.prefetch_related("tienda", "pieza").all()
    return render(request, 'inventario/lista_Inventario.html', {'inventario': inventario})


def editar_Inventario(request, id_Inventario):
    inventario= Inventario.objects.prefetch_related("tienda", "pieza").all()
    inventarioQuery= inventario.filter(id=id_Inventario).first()
    
    if request.method == "POST":
        formulario= DatosInventarioModelForms(request.POST, instance=inventarioQuery)
        
        if formulario.is_valid():
            
            
            formulario.save()
            messages.success(request, 'Editada la cantidad') 
            
            return redirect ("lista_ProductosTienda")

    
    else:
        formulario= DatosInventarioModelForms(instance=inventarioQuery)

    
    return render(request, 'inventario/editar_Inventario.html', {'formulario': formulario, 'inventarioQuery': inventarioQuery})


def datosInventario_delete(request, id_Inventario):
    inventario= Inventario.objects.prefetch_related("tienda", "pieza").all()
    inventarioQuery= inventario.filter(id=id_Inventario).first()
    
    try:
        inventarioQuery.delete()  
        messages.success(request, "Se ha eliminado los datos del inventario.")
        
        return redirect ("lista_ProductosTienda")
        
    except Exception as error:
        print(error)


def pieza_Buscar(request):
    
    
    if request.GET:
        formulario = BusquedaPiezaModelForm(request.GET)
        
        if formulario.is_valid():
            pieza= Pieza.objects.all() 
            
            # Obtenemos el nombre del formulario
            nombre = formulario.cleaned_data.get('nombre')
            
            # Filtramos las piezas por nombre
            piezaEncontrada= pieza.filter(nombre__icontains= nombre)
        
            return render(request, 'piezas/resultado_Busqueda.html',{"piezaEncontrada":piezaEncontrada})

    else:
        formulario = BusquedaPiezaModelForm()
        
    return render(request, 'piezas/pieza_Busqueda.html', {'formulario': formulario})
        
        


#Pagina de error 
def mi_error_404(request, exception= None):
    return render(request, 'errores/404.html', None, None, 404)

def mi_error_500(request, exception= None):
    return render(request, 'errores/500.html', None, None, 404)

