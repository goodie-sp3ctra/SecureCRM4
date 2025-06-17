from django import forms
from .models import Client

# LoginForm for user authentication
class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Username'
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label='Password'
    )

    class Meta:
        model = Client
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'address']  # Changed 'name' to 'first_name' and 'last_name'
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control'}),
        }
    def clean(self):
        cleaned_data = super().clean()
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')
        # Combine first_name and last_name into a single 'name' field
        if first_name and last_name:
            cleaned_data['name'] = f"{first_name} {last_name}"
        return cleaned_data

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = [
          'company_name',
          'contact_name',
          'contact_email',
          'phone',
          'address',
          'status',
        ]
        widgets = {
          'status': forms.Select(choices=Client.STATUS_CHOICES),
        }