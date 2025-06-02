import requests


class helper:
    
    def obtener_producto(id):
        
        headers = {    
                'Authorization': 'Bearer 3hlwlzqAPrQot5seySUvYGQ69kXHaY',
                   } 
        
        response = requests.get('http://0.0.0.0:8081/api/v1/obtener-producto/'
                                + str(id), headers=headers)
        
        
        producto = response.json()
        
        return producto
        