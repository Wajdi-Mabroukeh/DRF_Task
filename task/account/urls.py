from django.urls import path
from .views import RegisterView, LoginView, AccountList

urlpatterns = [
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('login/', LoginView.as_view(), name='auth_login'),
    path('users/', AccountList.as_view(), name='users_list'),
]