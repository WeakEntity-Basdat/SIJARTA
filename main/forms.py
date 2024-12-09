from django import forms

class OrderServiceForm(forms.Form):
    order_date = forms.DateField(widget=forms.SelectDateWidget())
    discount_code = forms.CharField(max_length=50, required=False)
    payment_method = forms.ChoiceField(choices=[
        ('MyPay', 'MyPay'),
        ('GoPay', 'GoPay'),
        ('OVO', 'OVO'),
        ('Dana', 'Dana'),
        ('Bank Transfer', 'Bank Transfer'),
        ('Cash on Delivery', 'Cash on Delivery'),
    ])