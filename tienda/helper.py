import requests


class helper:
    
    def obtener_producto(id):
        
        headers = {    
                'Authorization': 'Bearer 5cNtVstb83HtyRUBEQg0w6H62EqEob',
                   } 
        
        response = requests.get('http://0.0.0.0:8081/api/v1/obtener-producto/'
                                + str(id), headers=headers)
        
        
        producto = response.json()
        
        return producto
        