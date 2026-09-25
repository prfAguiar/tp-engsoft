from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import InvestmentSuggestionInputSerializer, ProjectionInputSerializer
from .services import calculate_projection, generate_investment_suggestion


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


class InvestmentSuggestionView(APIView):
    """
    Endpoint para sugerir divisão de investimentos e ativos com base em um montante indicado
    e no perfil de investidor (informado diretamente ou herdado do usuário autenticado).
    """

    def post(self, request):
        serializer = InvestmentSuggestionInputSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        amount = serializer.validated_data['amount']
        profile = serializer.validated_data.get('investor_profile')

        # Se o perfil não foi enviado no payload, tenta obter do usuário autenticado
        if not profile and request.user and request.user.is_authenticated:
            profile = getattr(request.user, 'investor_profile', None)

        if not profile:
            return Response(
                {
                    'error': (
                        'Perfil de investidor não informado. Forneça o campo "investor_profile" '
                        '(CONSERVATIVE, MODERATE, AGGRESSIVE) ou realize o questionário de perfil.'
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            # Obtém a carteira do usuário se estiver autenticado
            user_wallet = getattr(request.user, 'wallet', None) if request.user and request.user.is_authenticated else None

            result = generate_investment_suggestion(
                amount=amount,
                investor_profile=profile,
                wallet=user_wallet,
            )
            return Response(result, status=status.HTTP_200_OK)
        except ValueError as err:
            return Response({'error': str(err)}, status=status.HTTP_400_BAD_REQUEST)

class InvestmentCatalogView(APIView):
    """
    Endpoint para listar todos os investimentos cadastrados no sistema.
    Se o ativo possuir um 'ticker', busca dados em tempo real (preço atual, dividend yield) usando yfinance.
    """
    def get(self, request):
        from .models import Investment
        from .serializers import InvestmentSerializer
        
        investments = Investment.objects.all()
        serializer = InvestmentSerializer(investments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
