from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from Account.views.apiviews import UsuarioCriarListar, ContaCriarListar, ContaDetail, UsuarioDetail
# from Account.api.router import router

app_name = "Account"


urlpatterns = [
    path('token/', TokenObtainPairView.as_view()),
    path('token/verify/', TokenVerifyView.as_view()),
    path('refresh/', TokenRefreshView.as_view()),
    
    path('usuarios/', UsuarioCriarListar.as_view(), name="list-usuarios"),
    path('conta/', ContaCriarListar.as_view(), name="list-conta"),

    path('usuarios/<int:pk>', UsuarioDetail.as_view(), name="detail-usuarios"),
    path('conta/<int:pk>', ContaDetail.as_view(), name="detail-conta")
    
]

# urlpatterns += router.urls
