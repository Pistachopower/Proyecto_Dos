from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import *
from django.forms import ModelForm

from .helper import helper  


class RegistroForm(UserCreationForm): 
    roles = (
                (Usuario.CLIENTE, 'cliente'),
                (Usuario.VENDEDOR, 'vendedor'),
            )   
       
    rol = forms.ChoiceField(choices=roles)
       
    class Meta:
        model = Usuario
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2','rol')
        
    def clean(self): 
        cleaned_data = super().clean() 

        first_name = cleaned_data.get("first_name")
        last_name = cleaned_data.get("last_name")
        username = cleaned_data.get("username")

        # Longitudes mínimas y máximas
        MIN_LENGTH = 3
        MAX_LENGTH = 50

        if len(first_name) < MIN_LENGTH or len(first_name) > MAX_LENGTH:
            self.add_error('first_name', f'El nombre debe tener entre {MIN_LENGTH} y {MAX_LENGTH} caracteres.')

        if len(last_name) < MIN_LENGTH or len(last_name) > MAX_LENGTH:
            self.add_error('last_name', f'El apellido debe tener entre {MIN_LENGTH} y {MAX_LENGTH} caracteres.')

        if len(username) < MIN_LENGTH or len(username) > MAX_LENGTH:
            self.add_error('username', f'El nombre de usuario debe tener entre {MIN_LENGTH} y {MAX_LENGTH} caracteres.')

        return cleaned_data


            
    
        
    
    
        
        
        
class PiezaModelForm(ModelForm):
    class Meta:     #aqui sobreescribimos al padre ModelForm que tiene sus campos
        model = Pieza
        fields = ['nombre', 'version', 'referencia', 'estado', 'descripcion', 'marca', 'precio', 'anio']
        labels = { #esto es lo que va dentro del campo
            "nombre": ("Nombre de la pieza"),
            "descripcion": ("Descripcion de la pieza"),
            "anio": ("Año de la pieza"),
        }
        

        
        help_texts = {
            "nombre": ("10 caracteres como mínimo"),
            "descripcion":("Agrega una descripción de la pieza"),
        }
        
        #Definimos un campo Select para seleccionar el estado de la pieza
        estado = forms.ChoiceField(choices=Pieza.ESTADO,
                               initial="R")
        
        
    def clean(self): #este es para validar 
        
        super().clean() # comprueba las validaciones que tiene por defecto
        
        nombre = self.cleaned_data.get('nombre')
        version = self.cleaned_data.get('version')
        referencia = self.cleaned_data.get('referencia')
        descripcion = self.cleaned_data.get('descripcion')
        marca = self.cleaned_data.get('marca')
        precio = self.cleaned_data.get('precio')
        anio= self.cleaned_data.get('anio')
        
        
        compruebaPieza= Pieza.objects.filter(referencia=referencia).first()
        
        if compruebaPieza is not None:
            if self.instance is not None and compruebaPieza.id == self.instance.id:
                pass
            else:
                self.add_error('referencia', 'Ya existe una pieza con esa referencia')
        
        if len(nombre) < 3:
            self.add_error('nombre','Al menos debes indicar 3 caracteres')
            
        if len(version) < 3:
            self.add_error('version','Al menos debes indicar 3 caracteres')
            
        if len(referencia) < 3:
            self.add_error('referencia','Al menos debes indicar 3 caracteres')
 
        if len(descripcion) < 10:
            self.add_error('descripcion','Al menos debes indicar 10 caracteres')
            
        if len(marca) < 2: 
            self.add_error('marca','Al menos debes indicar 2 caracteres')
                      
        if precio < 0:
            self.add_error('precio','El precio no puede ser negativo o cero')
            
        if anio < 1900:
            self.add_error('anio','El año no puede ser menor a 1900')
                   
        #Siempre devolvemos el conjunto de datos.
        return self.cleaned_data            
        
       
class TiendaModelForm(ModelForm):
    class Meta:   
        model = Tienda
        fields = ['direccion', 'telefono', 'email']
        
    def clean(self): #este es para validar 
        super().clean() # comprueba las validaciones que tiene por defecto
        
        direccion = self.cleaned_data.get('direccion')
        telefono = self.cleaned_data.get('telefono')
        email = self.cleaned_data.get('email')
        
        #buscamos si hay una tienda con el numero que coloca el usuario
        compruebaTienda = Tienda.objects.filter(telefono=telefono).first()
        
        #si existe
        if compruebaTienda is not None:
            if self.instance is not None and compruebaTienda.id == self.instance.id:
                pass
            else:
                self.add_error('telefono', 'Ya existe un número de teléfono con esa tienda')
        
  
        # Rango de longitud permitido
        MIN_DIR = 5
        MAX_DIR = 100
        MIN_TEL = 7
        MAX_TEL = 15

        # Validación explícita con OR
        if len(direccion) < MIN_DIR or len(direccion) > MAX_DIR:
            self.add_error(
                'direccion',
                f'La dirección debe tener entre {MIN_DIR} y {MAX_DIR} caracteres.'
            )

        if len(telefono) < MIN_TEL or len(telefono) > MAX_TEL:
            self.add_error(
                'telefono',
                f'El teléfono debe tener entre {MIN_TEL} y {MAX_TEL} dígitos.'
            )
            
        # Validación de formato: solo dígitos
        if not telefono.isdigit():
            self.add_error('telefono', 'El teléfono solo debe contener números.')
        
        # Verifica si el correo está vacío y tiene mayúsculas
        if email and email != email.lower():
            self.add_error('email','No puede conteneder mayúsculas')
        
        return self.cleaned_data  

        
class CuentaBancariaModelForm(ModelForm):
    class Meta:   
        model = CuentaBancaria
        fields = ['iban', 'banco', 'moneda']   
        
        moneda = forms.ChoiceField(choices=CuentaBancaria.MONEDA,
                               initial="EUR")
        
        help_texts = {
            "iban": ("Ejemplo de IBAN: ES1234567890123456789012"),
        }
        
    def clean(self):
        super().clean() 
        
        iban = self.cleaned_data.get('iban')
        banco = self.cleaned_data.get('banco')
        
        compruebaCuenta = CuentaBancaria.objects.filter(iban=iban).first()
        
        if compruebaCuenta is not None:
            if self.instance is not None and compruebaCuenta.id == self.instance.id:
                pass
            else:
                self.add_error('iban', 'Ya existe una cuenta bancaria con ese IBAN')
                
        if len(iban) < 22 or len(iban) > 34:
            self.add_error('iban', 'El IBAN debe tener entre 15 y 34 caracteres')
            
        if len(banco) < 3:
            self.add_error('banco','Al menos debes indicar 3 caracteres')
            
        return self.cleaned_data    
    
    
class DatosVendedorModelForm(ModelForm):
    class Meta:   
        model = DatosVendedor
        fields = ['direccion', 'facturacion']   
        
        
    def clean(self):
        super().clean() 
        
        direccion = self.cleaned_data.get('direccion')
        facturacion = self.cleaned_data.get('facturacion')
                
        if len(direccion) < 2:
            self.add_error('direccion', 'La dirección debe tener al menor 2 caracteres')
            
        if len(facturacion) < 3:
            self.add_error('facturacion','Al menos debes indicar 3 caracteres')
            
        return self.cleaned_data         
    
    
    
class DatosVendedorModelForms_Editar(ModelForm):
    class Meta:
        model = DatosVendedor 
        fields = ['direccion', 'facturacion']  
        help_texts = {
            'direccion' : ("Direccion del vendedor"),
            'facturacion': ("Facturacion del vendedor"),
        }      

"""
En la vista, paso el objeto request manualmente al formulario porque necesito saber qué usuario está logueado. 
En el formulario, saco el request del diccionario kwargs usando .pop("request"), para que Django no se queje, 
y lo guardo en self.request para luego usar self.request.user y filtrar las tiendas que puede ver ese usuario.

"""     
        
class DatosVendedorModelForms(ModelForm):
    class Meta:
        model = Producto_Tienda 
        fields = ['tienda', 'pieza','stock', 'precio']  
        help_texts = {
            'tienda' : ("Selecciona la tienda"),
            'pieza' : ("Selecciona la pieza"),
            'stock': ("Indica la cantidad"),
            'precio': ("Indica el precio"),
        }  
        
    #se usa esto para obtener solo las tiendas que puede ver el usuario loggeado
    def __init__(self, *args, **kwargs):
        self.request= kwargs.pop("request")
        super(DatosVendedorModelForms, self).__init__(*args, **kwargs)
        
        #hacemos un filtro para que solo vea las tiendas que le pertenecen al vendedor
        tiendasDisponibles= Tienda.objects.filter(vendedor= self.request.user.vendedor).all()
        self.fields["tienda"]= forms.ModelChoiceField(
            queryset= tiendasDisponibles, 
            widget=forms.Select,
            required= True,
            empty_label= "Ninguna"
        )
        
    def clean(self):
        super().clean() 
        
        stock = self.cleaned_data.get('stock')
        precio = self.cleaned_data.get('precio')
        
        if stock < 0:
            self.add_error('stock','El stock no puede ser negativo')
                
        if precio < float(0):
            self.add_error('precio', 'El precio no puede ser un valor negativo')
                        
        return self.cleaned_data 
        
        
        
        
        
        
class DatosInventarioEditarModelForms(ModelForm):
    class Meta:
        model = Producto_Tienda 
        fields = ['tienda','pieza','stock']  
        help_texts = {
            'cantidad': ("Indica el stock"),
        }  
            
        
        
        
#busqueda de piezas
class BusquedaPiezaModelForm(forms.Form):  
    nombre = forms.CharField(required=False, label="Nombre")
    
    
class PedidoModelForm(ModelForm):
        class Meta:
            model = Pedido 
            fields = ['direccion']
            

            
            labels = {
                "direccion": ("Direccion de entrega"),
            }
            

            
class AnadirProductoTiendaModelForm(forms.Form):
    #datos que escribe el usuario
    cantidad = forms.IntegerField (required=True, label="Cantidad")
    
    def clean(self):
        super().clean()
    
        cantidad = self.cleaned_data.get('cantidad')
        
    
        #comprobamos si la cantidad es menor que el stock
        if cantidad <= 0:
            self.add_error('cantidad', 'La cantidad debe ser un número positivo.')

        elif cantidad > self.producto_tienda_obj.stock:
            self.add_error('cantidad', 'La cantidad debe ser menor que ' + str(self.producto_tienda_obj.stock))


        return self.cleaned_data  

    def __init__ (self, *args, **kwargs):
        # Guardamos el objeto recibido desde la vista
        self.producto_tienda_obj = kwargs.pop("producto_tienda_obj")
        super(AnadirProductoTiendaModelForm, self).__init__(*args, **kwargs)
        
        
class BusquedaAvanzadaPiezaForm(forms.Form):
    direccion= forms.CharField(required=False,  label="Dirección")
    precioMen= forms.FloatField(required=False, label="Precio mínimo de la pieza")
    precioMay= forms.FloatField(required=False, label="Precio máximo de la pieza")
    stock= forms.IntegerField(required=False, label="Stock de la pieza")
    
    def clean(self):
        super().clean()
        
        #Obtenemos los campos 
        direccion = self.cleaned_data.get('direccion')
        precioMen = self.cleaned_data.get('precioMen')
        precioMay = self.cleaned_data.get('precioMay')
        stock = self.cleaned_data.get('stock')

        #Validamos que al menos uno esté lleno
        if not direccion and precioMen is None and precioMay is None and stock is None:
            self.add_error('direccion', 'El campo no puede estar vacío')
            self.add_error('precioMen', 'El campo no puede estar vacío')
            self.add_error('precioMay', 'El campo no puede estar vacío')
            self.add_error('stock', 'El campo no puede estar vacío')
            
        
                # Validamos que los valores numéricos no sean negativos
        if precioMen is not None and precioMen < 0:
            self.add_error('precioMen', 'El precio menor no puede ser negativo.')

        if precioMay is not None and precioMay < 0:
            self.add_error('precioMay', 'El precio mayor no puede ser negativo.')

        if stock is not None and stock < 0:
            self.add_error('stock', 'La cantidad no puede ser negativa.')
            
        return self.cleaned_data
        
        
class EditarLineaPedidoForm(forms.ModelForm):
    class Meta:
        model = LineaPedido
        fields = ['cantidad']
        labels = {
                'cantidad': ("Indica la cantidad de la pieza"),
            }
        
        
    def clean(self):
        super().clean()
        
        cantidad = self.cleaned_data.get('cantidad')
        
        if cantidad is not None and cantidad < 0:
            self.add_error('cantidad', 'La cantidad no puede ser negativa.')
        
        
        
        
class FinalizarPedidoForm(ModelForm):
    class Meta:
        model = Pedido
        fields = ['direccion']
        labels = {
            'direccion': ("Indica la dirección de envío"),
        }

    def clean(self):
        cleaned_data = super().clean()
        pedido = self.instance  # El pedido que se está finalizando

        # Validar stock de cada línea del pedido
        for linea in pedido.pedido_lineaPedido.all():
            
            producto = Producto_Tienda.objects.get(tienda=linea.tienda, pieza=linea.pieza)
            if producto.stock < linea.cantidad:
                self.add_error(
                    None,  # Error general, no de un campo específico
                    f"No hay suficiente stock para la pieza '{linea.pieza.nombre}' en la tienda '{linea.tienda.direccion}'. Stock disponible: {producto.stock}, solicitado: {linea.cantidad}"
                )
        return cleaned_data
        
        
class CrearProductoTerceroForm(forms.Form):
    nombre= forms.CharField(required=False,  label="Nombre del producto")
    precio= forms.FloatField(required=False, label="Precio de la pieza")
    
 

class NombreProductoForm(forms.Form):
    nombre = forms.CharField(label="Nombre del producto",
                             required=True, 
                             max_length=50,
                             help_text="50 caracteres como máximo") 

            
            
            
            
    
    
    
        
        
            
        
        

            
        
        
        
        
        
