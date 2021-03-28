from django.urls import path
from .views import (
    RegisterView, LoginView, AccountAddressView,
    AccountInfoView, AccountListView
)

urlpatterns = [
    path('^register', RegisterView.as_view(), name='auth_register'),
    path('^login', LoginView.as_view(), name='auth_login'),
    path('^users', AccountListView.as_view(), name='users_list'),
    path('^user', AccountInfoView.as_view(), name='user_basic_info'),
    path('^user/address', AccountAddressView.as_view(), name='user_addresses'),

]