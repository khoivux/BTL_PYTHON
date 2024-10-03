from django import forms

PRICE_CHOICES = [
    ('100', 'Up to $100'),
    ('200', 'Up to $200'),
    ('300', 'Up to $300'),
    ('400', 'Up to $400'),
]

class HomestayFilterForm(forms.Form):
    min_price = forms.DecimalField(required=False, decimal_places=2, max_digits=10, label='Min Price')
    max_price = forms.DecimalField(required=False, decimal_places=2, max_digits=10, label='Max Price')
   