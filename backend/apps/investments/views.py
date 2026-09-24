from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import ProjectionInputSerializer
from .services import calculate_projection


class ProjectionSimulationView(APIView):
    """
    Endpoint para projeção de rendimento de investimentos ao longo do tempo.
    """

    def post(self, request):
        serializer = ProjectionInputSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        result = calculate_projection(**serializer.validated_data)
        return Response(result, status=status.HTTP_200_OK)
