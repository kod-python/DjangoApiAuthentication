# myapp/urls.py
from django.urls import path
from .views import SignupView
# from .views import LoginView
# from .views import UserLoginView, UserSignupView
from .views import UserLoginView
from .views import BatchUserLoginView
from .views import PasswordResetRequestView, PasswordResetConfirmView
# from .views import SendResetEmailView
from .views import RequestResetEmailView, ConfirmResetView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    # path('login/', LoginView.as_view(), name='login'),
    
    # path('signup/', UserSignupView.as_view(), name='signup'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('batch-login/', BatchUserLoginView.as_view(), name='batch-login'),
    path('password_reset/', PasswordResetRequestView.as_view(), name='password_reset_request'),
    path('password_reset/confirm/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    #  path('send-reset-email/', SendResetEmailView.as_view(), name='send-reset-email'),
      path('request-reset-email/', RequestResetEmailView.as_view(), name='request-reset-email'),
    path('confirm-reset/', ConfirmResetView.as_view(), name='confirm-reset'),
]







# from django.urls import path
# from .views import SignupView, LoginView
# from .views import AuthenticationListCreateView,AuthenticationeRetrieveUpdateDestroyView
# urlpatterns = [
#     path('authen/', AuthenticationListCreateView.as_view(), name='authentication-list-create'),
#     path('signup/', SignupView.as_view(), name='signup'),
#     path('login/', LoginView.as_view(), name='login'),
#     path('authen/<int:pk>/', AuthenticationeRetrieveUpdateDestroyView.as_view(), name='authentication-detail'),
# ]
