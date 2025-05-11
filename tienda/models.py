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


#cliente y usuario usara los atributos de Usuario 
class Cliente(models.Model):
    
    usuario = models.OneToOneField(Usuario, on_delete= models.CASCADE)
    
    def __str__(self):
        return self.usuario.username  
    


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
    
    
    
class Tienda(models.Model):
    direccion = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15)
    email= models.EmailField()
    vendedor= models.ForeignKey(Vendedor, on_delete= models.CASCADE, default=None, null=True)
    piezas= models.ManyToManyField(Pieza, through='Inventario',related_name="tienda_Inventarios")
    
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
    
    

class Inventario(models.Model):
    tienda= models.ForeignKey(Tienda, on_delete= models.CASCADE)
    pieza= models.ForeignKey(Pieza, on_delete= models.CASCADE)
    cantidad= models.IntegerField()
    

    
    
class Pedido(models.Model):
    ESTADO= [("P", "Pendiente"), ("C", "Completado"), ("A", "Anulado")]
    estado= models.CharField(max_length=1, choices=ESTADO, default="P")
    fecha= models.DateField(null=True, blank=True)
    direccion= models.CharField(max_length=100)
    #many to one
    pieza= models.ForeignKey(Pieza, on_delete=models.CASCADE)
    cliente= models.ForeignKey(Cliente, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.direccion
    

    
    


    
    
    