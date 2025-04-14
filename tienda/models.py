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
    
    
    def __str__(self):
        return self.direccion


class CuentaBancaria(models.Model):
    ibam = models.CharField(max_length=25)
    banco = models.CharField(max_length=25)
    MONEDA= [("EUR", "Euro"), ("DOL", "Dolar"), ("LIB", "Libra")]
    moneda = models.CharField(max_length=3, choices=MONEDA, default="E")
    cliente= models.OneToOneField(Cliente, on_delete=models.CASCADE)
    
    
    def __str__(self):
        return self.banco

class DatosPerfil(models.Model):
    direccionFacturacion = models.CharField(max_length=100)
    vendedor= models.OneToOneField(Vendedor, on_delete=models.CASCADE)
    