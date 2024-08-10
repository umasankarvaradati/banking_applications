
from django import forms
from .models import Customer

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = [
            'full_name',
            'address',
            'mobile_no',
            'email_id',
            'account_type',
            'initial_balance',
            'dob',
            'id_proof'
        ]
