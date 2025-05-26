from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .forms import *

@api_view(['GET'])
def listar_piezas(request):
    listaPiezas = Pieza.objects.all()
    serializer = PiezaSerializer(listaPiezas, many=True)
    return Response(serializer.data)
