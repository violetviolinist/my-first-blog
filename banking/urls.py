from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^create/', views.create_customer, name = 'create_customer'),
    url(r'^login/', views.login_customer, name = 'login_customer'),
    url(r'^logout/', views.logout_customer, name = 'logout_customer'),
    url(r'^checksession', views.check_session, name = 'check_session'),
    url(r'^delete', views.delete_customer, name = 'delete_customer'),
    url(r'^get_balance', views.get_balance, name = 'get_balance'),
    url(r'^withdraw', views.withdraw, name = 'withdraw'),
    url(r'^deposit', views.deposit, name = 'deposit')
]