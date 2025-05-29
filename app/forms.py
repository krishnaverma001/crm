from django import forms
from .models import Customer

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'John'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Doe'}),
            'email': forms.EmailInput(attrs={'placeholder': 'johndoe@gmail.com'}),
            'phone': forms.TextInput(attrs={'placeholder': '0123456789'}),
            'address': forms.TextInput(attrs={'placeholder': '1234 Baker Street'}),
            'city': forms.TextInput(attrs={'placeholder': 'New Delhi'}),
            'state': forms.TextInput(attrs={'placeholder': 'Delhi'}),
            'pincode': forms.TextInput(attrs={'placeholder': '203910'}),
        }