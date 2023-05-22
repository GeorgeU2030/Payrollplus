from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from .models import Company

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'input form-control ',
        'placeholder':'Ingrese su Email',
        'id':'input_email',
        'style': 'font-weight: 600;',
    }))
    name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id':'input_name',
        'maxlength':100,
        'style': 'font-weight: 600;',
    }))

    address = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id':'input_address',
        'maxlength':100,
        'style': 'font-weight: 600;',
    }))

    city = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id':'input_city',
        'maxlength':100,
        'style': 'font-weight: 600;',
    }))
    website = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id':'input_website',
        'maxlength':255,
        'style': 'font-weight: 600;',
    }))

    identification = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id':'input_identification',
        'maxlength':30,
        'style': 'font-weight: 600;',
    }))

    typecompany = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id':'input_typecompany',
        'maxlength':30,
        'style': 'font-weight: 600;',
    }))
    
    profilePicture = forms.ImageField(widget=forms.FileInput(attrs={
        'class': 'form-control',
        'id':'imageInput',
    }), required=False)

    password1 = forms.CharField(strip=False, widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Crea una contraseña',
        'autocomplete': 'current-password',
        'id':'input_pass1',
        'style': 'font-weight: 600;',
    }))

    password2 = forms.CharField(strip=False, widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Confirma tu contraseña',
        'autocomplete': 'current-password',
        'id':'input_pass2',
        'style': 'font-weight: 600;',
    }))

    class Meta:
        model = Company
        fields = ("email","name","password1","password2","website", 'address','city')
       


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = Company
        fields = ("email", )


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label='Correo electrónico', widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Correo electrónico',
        'style':'border-radius:1rem; text-align:end; font-weight: 600;',
    }))
    password = forms.CharField(label='Contraseña', strip=False, widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Contraseña',
        'autocomplete': 'current-password',
         'style':'border-radius:1rem; text-align:end; font-weight: 600;',
    }))
    
    error_messages = {
        'invalid_login': 'Correo electrónico o contraseña incorrectos',
        'inactive': 'Esta cuenta no está activa.',
        
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = ''
        self.fields['username'].widget.attrs.update({
            'placeholder': 'Correo electrónico',
            'class': 'form-control',
        })
        self.fields['password'].label = ''
        self.fields['password'].widget.attrs.update({
            'placeholder': 'Contraseña',
            'class': 'form-control',
        })