from django.urls import path
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView, TokenVerifyView)

from Account.views.apiviews import (ContaCriarListar, ContaDetail,
                                    UsuarioCriarListar, UsuarioDetail)

# from Account.api.router import router

app_name = "Account"


urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name="token"),
    path('token/verify/', TokenVerifyView.as_view(), name="token-verify"),
    path('refresh/', TokenRefreshView.as_view(), name="token-refresh"),
    path('usuarios/', UsuarioCriarListar.as_view(), name="list-usuarios"),
    path('conta/', ContaCriarListar.as_view(), name="list-account"),
    path('usuarios/<int:pk>', UsuarioDetail.as_view(), name="detail-usuarios"),
    path('conta/<int:pk>', ContaDetail.as_view(), name="detail-account"),
]

# urlpatterns += router.urls
