from django.urls import path
from .views import withdraw_funds, withdrawal_history,transactions,earnings,dashboard,request_withdrawal

urlpatterns = [
    # path("withdraw/", withdraw_funds, name="withdraw_funds"),
    path("history/", withdrawal_history, name="withdrawal_history"),
    # path('transactions/', transactions, name='transactions'),
    path('withdraw/', request_withdrawal, name='withdraw_funds'),
    # path('earnings/', earnings, name='earnings'),
    path('earnings/', dashboard, name='earnings'),
]


# from django.urls import path
# from . import views

# urlpatterns = [
#     path('transactions/', views.transactions, name='transactions'),
#     path('earnings/', views.earnings, name='earnings'),
# ]
