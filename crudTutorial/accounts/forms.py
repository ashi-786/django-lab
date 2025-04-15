from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# Register User
class CreateUserForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control mb-3'
        })
        self.fields['password1'].widget.attrs.update({
            'id': 'pass1',
            'class': 'form-control',
            'aria-describedby': "basic-addon1"
        })
        self.fields['password2'].widget.attrs.update({
            'id': 'pass2',
            'class': 'form-control',
            'aria-describedby': "basic-addon2"
        })

    username = forms.CharField(max_length=255)
    password1 = forms.CharField(max_length=255, widget=forms.PasswordInput)
    password2 = forms.CharField(max_length=255, widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    # def clean_password1(self):
    #     return self.cleaned_data.get("password1")