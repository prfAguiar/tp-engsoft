from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import InvestorProfileEvaluationView, InvestorProfileQuizQuestionsView, RegisterView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/quiz/questions/', InvestorProfileQuizQuestionsView.as_view(), name='investor-quiz-questions'),
    path('profile/quiz/evaluate/', InvestorProfileEvaluationView.as_view(), name='investor-quiz-evaluate'),
]
