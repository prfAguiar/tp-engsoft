from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class InvestorProfileQuizAnswerSerializer(serializers.Serializer):
    question_id = serializers.CharField(max_length=50)
    score = serializers.IntegerField(
        min_value=1,
        max_value=3,
        help_text="Pontuação da resposta escolhida (entre 1 e 3)",
    )


class InvestorProfileQuizInputSerializer(serializers.Serializer):
    answers = serializers.ListField(
        child=InvestorProfileQuizAnswerSerializer(),
        allow_empty=False,
        help_text="Lista de respostas do questionário de perfil",
    )

    def validate_answers(self, value):
        if len(value) != 4:
            raise serializers.ValidationError(
                "O questionário deve conter exatamente 4 respostas."
            )
        question_ids = [item['question_id'] for item in value]
        if len(question_ids) != len(set(question_ids)):
            raise serializers.ValidationError(
                "Não é permitido repetir respostas para a mesma pergunta."
            )
        return value


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'first_name', 'last_name')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['email'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'investor_profile')
        read_only_fields = ('id', 'email')
