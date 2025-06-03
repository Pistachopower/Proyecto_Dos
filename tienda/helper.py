import requests


class helper:
    
    def obtener_producto(id):
        
        headers = {    
                'Authorization': 'Bearer sq2fpC4hCklRpF6HGI8B2kGRxJH95N',
                   } 
        
        response = requests.get('http://0.0.0.0:8081/api/v1/obtener-producto/'
                                + str(id), headers=headers)
        
        
        producto = response.json()
        
        return producto
        