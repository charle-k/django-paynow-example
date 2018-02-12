from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^my_profile/', views.my_profile, name='my_profile'),
    #url(r'^cashier/', views.cashier_index, name='cashier'),
    url(r'^confirmed_payments/', views.confirmed_payments,
        name='confirmed_payments'),
    url(r'^unconfirmed_payments/', views.unconfirmed_payments,
        name='unconfirmed_payments'),


    url(r'^paynow_payment/$', views.paynow_payment, name="paynow_payment"),
    #
    url(r'^paynow_return/(?P<order_id>\w+)$', views.paynow_return,
            name="paynow_return"),
    #
    url(r'^paynow_update/(?P<order_id>\w+)$', views.paynow_update,
        name="paynow_update"),
    ]