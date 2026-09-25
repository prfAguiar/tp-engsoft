from django.urls import path

from .views import InvestorProfileEvaluationView, InvestorProfileQuizQuestionsView

urlpatterns = [
    path('profile/quiz/questions/', InvestorProfileQuizQuestionsView.as_view(), name='investor-quiz-questions'),
    path('profile/quiz/evaluate/', InvestorProfileEvaluationView.as_view(), name='investor-quiz-evaluate'),
]
