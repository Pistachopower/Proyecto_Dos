import requests


class helper:
    #NO SE ESTÁ IMPLEMENTANDO EL MÉTODO DE OBTENER PRODUCTOS DE TERCEROS
    def obtener_producto_terceros_select():
        
        headers = {
            
                'Authorization': 'Bearer dulmwogNLx4iwVhfpZBTXR1RtTkq3g',
                   
                   } 
        
        response = requests.get('http://0.0.0.0:8081/api/v1/listar_productosTercero/',headers=headers)
        
        producto_tercero = response.json()