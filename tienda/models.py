from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    ADMINISTRADOR = 1
    CLIENTE = 2
    VENDEDOR = 3
    ROLES = (
        (ADMINISTRADOR, 'administardor'),
        (CLIENTE, 'cliente'),
        (VENDEDOR, 'vendedor'),
    )
    
    rol  = models.PositiveSmallIntegerField(
        choices=ROLES,default=2
    )



class Vendedor(models.Model):
    
    usuario = models.OneToOneField(Usuario, on_delete= models.CASCADE)
    
    def __str__(self):
        return self.usuario.username
    
    
class Pieza(models.Model):
    nombre= models.CharField(max_length=100)
    version= models.CharField(max_length=100)
    referencia= models.CharField(max_length=100)
    ESTADO = [("N", "Nueva"), ("R", "Recuperada"), ("REC", "Reconstruida")]
    estado = models.CharField(max_length=3, choices=ESTADO)
    descripcion= models.TextField()
    marca= models.CharField(max_length=100)
    precio= models.FloatField(default=1.0) #QUITAR
    anio= models.IntegerField()
    
    def __str__(self):
        return self.nombre


class Cliente(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    # Relación muchos a muchos con Pieza a través de Pedido
    
    def __str__(self):
        return self.usuario.username
    
    
    
class Tienda(models.Model):
    direccion = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15)
    email= models.EmailField()
    vendedor= models.ForeignKey(Vendedor, on_delete= models.CASCADE, default=None, null=True)
    piezas= models.ManyToManyField(Pieza, through='Producto_Tienda',related_name="tienda_Inventarios")
    
    def __str__(self):
        return self.direccion


class CuentaBancaria(models.Model):
    iban = models.CharField(max_length=25)
    banco = models.CharField(max_length=25)
    MONEDA= [("EUR", "Euro"), ("DOL", "Dolar"), ("LIB", "Libra")]
    moneda = models.CharField(max_length=3, choices=MONEDA, default="E")
    cliente= models.OneToOneField(Cliente, on_delete=models.CASCADE)
    
    
    def __str__(self):
        return self.banco

class DatosVendedor(models.Model):
    direccion = models.CharField(max_length=100)
    facturacion = models.CharField(max_length=100)
    vendedor= models.OneToOneField(Vendedor, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.direccion
    
    
#anteriormente inventario
class Producto_Tienda(models.Model):
    tienda= models.ForeignKey(Tienda, on_delete= models.CASCADE)
    pieza= models.ForeignKey(Pieza, on_delete= models.CASCADE)
    cantidad= models.IntegerField() #cambiar cantidad por stock
    precio= models.FloatField(default=1.0) 
    

    
class Pedido(models.Model):
    ESTADO = [
        ("P", "Pendiente"),
        ("C", "Completado"),
        ("A", "Anulado")
    ]
    estado = models.CharField(max_length=1, choices=ESTADO, default="P")
    fecha = models.DateTimeField(auto_now_add=True) #asigna la fecha y hora actual al crear el pedido
    direccion = models.CharField(max_length=100)

    
    # Relación muchos a muchos utilizando la tabla Pedido como intermedia
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='pedidos')


    
    def __str__(self):
        return f"Pedido de {self.cliente.usuario.username}"
    
    
class LineaPedido(models.Model):
    pedido= models.ForeignKey(Pedido, on_delete= models.CASCADE, related_name="pedido_lineaPedido")
    pieza= models.ForeignKey(Pieza, on_delete= models.CASCADE, related_name="pieza_lineaPedido") 
    tienda= models.ForeignKey(Tienda, on_delete= models.CASCADE, related_name="tienda_lineaPedido")
    precio= models.FloatField(default=1.0) 
    cantidad= models.IntegerField() 


    


    
    


    
    
    