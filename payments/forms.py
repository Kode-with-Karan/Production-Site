from django import forms

class WithdrawalForm(forms.Form):
    amount = forms.DecimalField(min_value=10.00, max_digits=10, decimal_places=2)