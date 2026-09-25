from rest_framework import serializers


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
