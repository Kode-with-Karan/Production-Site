from django.urls import path
from django.shortcuts import render
from . import views
urlpatterns = [
    path('start/<str:amount>', views.start_payment, name='start_payment'),
    path('complete/', views.complete_payment, name='complete_payment'),
    path('cancel/', lambda request: render(request, 'payments/cancel.html'), name='cancel_payment'),
    path('success/', views.paypal_success, name='paypal_success'),
    path('withdraw/', views.request_withdrawal, name='request_withdrawal'),
    path('withdraw/success/', views.withdrawal_success, name='withdrawal_success'),  # ✅ Add this

]


# from django.urls import path
# from . import views

# urlpatterns = [
#     path('transactions/', views.transactions, name='transactions'),
#     path('earnings/', views.earnings, name='earnings'),
# ]
