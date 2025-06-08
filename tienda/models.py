from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    ADMINISTRADOR = 1
    CLIENTE = 2
    VENDEDOR = 3
    ROLES = (
        (ADMINISTRADOR, 'administrador'),
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
    precio= models.FloatField(default=1.0) 
    anio= models.IntegerField()
    
    def __str__(self):
        return self.nombre


class Cliente(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    
    #se pone en decimal para que se pueda relejar la devolución del precio de la pieza
    puntos = models.FloatField(default=0.0)  # Puntos del cliente al momento de la devolución
    
    
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
    stock= models.IntegerField() 
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



class Pago(models.Model):
    #Un pago está asociado a un solo pedido, y un pedido solo puede tener un pago
    pedido = models.OneToOneField(Pedido, on_delete=models.CASCADE, related_name="pago")
    
    #El pago se hace desde una cuenta bancaria, así que conectamos con CuentaBancaria usando ForeignKey
    cuenta_bancaria = models.ForeignKey(CuentaBancaria, on_delete=models.CASCADE, related_name="pagos")
    monto = models.FloatField()
    fecha_pago = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pago de {self.monto} € por {self.pedido}"
    
class Devolucion(models.Model):
    #puedo tener muchas devuluciones que apuntan a una misma linea pedido (one to many)
    lineaPedido = models.OneToOneField(LineaPedido, on_delete=models.CASCADE, related_name="devoluciones")
    
    #cliente puede tener muchas devoluciones (one to many)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name="devoluciones")
    fecha_devolucion = models.DateTimeField(auto_now_add=True)
    ESTADO = [
        ("P", "Pendiente"),
        ("R", "Resuelta")
    ]
    estado = models.CharField(max_length=1, choices=ESTADO, default="P")

    def __str__(self):
        return f"Devolución del pedido {self.pedido.id} - Motivo: {self.estado}"

    


    
    


    
    
    