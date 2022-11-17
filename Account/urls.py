from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from Account.views.apiviews import CriarUsuario, CriarConta


app_name = "Account"


urlpatterns = [
    path('token/',TokenObtainPairView.as_view()),
    path('token/verify/',TokenVerifyView.as_view()),
    path('refresh/',TokenRefreshView.as_view()),
    
    path('usuarios/',CriarUsuario.as_view()),
    path('conta/',CriarConta.as_view())
]
