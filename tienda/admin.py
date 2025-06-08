from django.contrib import admin

# Register your models here.
from .models import *
admin.site.register(Usuario)
admin.site.register(Cliente)
admin.site.register(Vendedor)
admin.site.register(Pieza)
admin.site.register(Tienda)
admin.site.register(CuentaBancaria)
admin.site.register(DatosVendedor)
admin.site.register(Producto_Tienda)
admin.site.register(Pedido)
admin.site.register(LineaPedido)
admin.site.register(Pago)
admin.site.register(Devolucion)

