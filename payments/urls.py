
from django.urls import path

from . import views

app_name = 'payments'
urlpatterns = [
    path('', views.index, name='index'),
    path('my_profile/', views.my_profile, name='my_profile'),
    path('confirmed_payments/', views.confirmed_payments, name='confirmed_payments'),
    path('paynow_payment/', views.paynow_payment, name="paynow_payment"),
    path('paynow_return/<int:payment_id>/', views.paynow_return, name="paynow_return"),
    path('paynow_update/<int:order_id>/', views.paynow_update, name="paynow_update"),
]