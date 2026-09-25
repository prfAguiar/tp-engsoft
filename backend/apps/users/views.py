from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import InvestorProfileQuizInputSerializer
from .services import QUIZ_QUESTIONS, calculate_investor_profile


class InvestorProfileQuizQuestionsView(APIView):
    """
    Endpoint para listar as perguntas do questionário de perfil de investidor.
    """

    def get(self, request):
        return Response({'questions': QUIZ_QUESTIONS}, status=status.HTTP_200_OK)


class InvestorProfileEvaluationView(APIView):
    """
    Endpoint para submeter o questionário, calcular o perfil e,
    se autenticado, atualizar o perfil de investidor do usuário.
    """

    def post(self, request):
        serializer = InvestorProfileQuizInputSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        scores = [item['score'] for item in serializer.validated_data['answers']]
        result = calculate_investor_profile(scores)

        # Se o usuário estiver autenticado, salva seu perfil no banco
        if request.user and request.user.is_authenticated:
            request.user.investor_profile = result['profile']
            request.user.save(update_fields=['investor_profile'])
            result['saved'] = True
        else:
            result['saved'] = False

        return Response(result, status=status.HTTP_200_OK)

from rest_framework import generics
from rest_framework.permissions import AllowAny
from .serializers import UserRegistrationSerializer

class RegisterView(generics.CreateAPIView):
    queryset = UserRegistrationSerializer.Meta.model.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserRegistrationSerializer
