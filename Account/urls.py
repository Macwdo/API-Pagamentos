from django.urls import path
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView, TokenVerifyView)

from Account.views.apiviews import (AccountCreateList, AccountDetail,
                                    UserCreateList, UserDetail, TransferCreateList)

# from Account.api.router import router

app_name = "Account"


urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name="token"),
    path('token/verify/', TokenVerifyView.as_view(), name="token-verify"),
    path('refresh/', TokenRefreshView.as_view(), name="token-refresh"),
    path('usuarios/', UserCreateList.as_view(), name="list-usuarios"),
    path('conta/', AccountCreateList.as_view(), name="list-account"),
    path('usuarios/<int:pk>', UserDetail.as_view(), name="detail-usuarios"),
    path('conta/<int:pk>', AccountDetail.as_view(), name="detail-account"),
    path('transferencia/', TransferCreateList.as_view(), name="list-transfer")
]

# urlpatterns += router.urls
