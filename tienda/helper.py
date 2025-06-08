import requests


class helper:
    
    def obtener_producto(id):
        
        headers = {    
                'Authorization': 'Bearer y10KqCW7ajqPQQXpTYH39zzR3a0ff3',
                   } 
        
        response = requests.get('http://0.0.0.0:8081/api/v1/obtener-producto/'
                                + str(id), headers=headers)
        
        
        producto = response.json()
        
        return producto
        