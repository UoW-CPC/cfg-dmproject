from django import forms

class RegForm(forms.Form):
        firstname = forms.CharField(label='First name:', max_length=100)
        lastname = forms.CharField(label='Last name:', max_length=100)
        email = forms.EmailField() #.CharField(label='Email:', max_length=100)
        username = forms.CharField(label='User name:', max_length=100)
        password = forms.CharField(widget=forms.PasswordInput()) #forms.CharField(label='Password:', max_length=100)
        
