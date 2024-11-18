from django import forms
from .models import ServiceOrder

class ServiceOrderForm(forms.ModelForm):
    class Meta:
        model = ServiceOrder
        fields = ['order_date', 'discount_code', 'total_payment', 'payment_method']
        widgets = {
            'order_date': forms.DateInput(attrs={'type': 'date'}),
            'total_payment': forms.NumberInput(attrs={'step': '0.01'}),
        }
