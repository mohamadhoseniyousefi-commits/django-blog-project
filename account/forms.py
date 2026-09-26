from django import forms
from django.contrib.auth.forms import authenticate
from django.contrib.auth.models import User
from django.forms import ValidationError
from .models import Profile


class Login_form(forms.Form):
    username = forms.CharField(max_length=40, widget=forms.TextInput(attrs={'class': 'input100','placeholder': 'username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input100','placeholder': 'Password'}))

    def clean(self):
        cleaned_data = super().clean()
        user = authenticate(username=cleaned_data.get('username'), password=cleaned_data.get('password'))
        if user is not None:
            return cleaned_data
        raise ValidationError('The password or username is incorrect.')





class edit_user_form(forms.ModelForm):
    class Meta:
        model =User
        fields = ['first_name','last_name','email',]

        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'First Name'
            }),

            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Last Name'
            }),

            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email'
            }),
        }


class edit_profile_form(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['name_father', 'meliname', 'image']

        widgets = {
            'name_father': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Name Father'
            }),

            'meliname': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Meli Name'
            }),

            'image': forms.FileInput(attrs={
                'class': 'form-control'
            }),
        }








class Register_form(forms.Form):
    username = forms.CharField(max_length=25, widget=forms.TextInput(attrs={'class': 'input100', 'placeholder': 'Username'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'input100', 'placeholder': 'Email'}))
    password = forms.CharField(max_length=18,widget=forms.PasswordInput(attrs={'class': 'input100', 'placeholder': 'Password'}))
    password2 = forms.CharField(max_length=18,widget=forms.PasswordInput(attrs={'class': 'input100', 'placeholder': 'Confirm Password'}))



    def clean_username(self):
        username = self.cleaned_data.get('username')

        if User.objects.filter(username=username).exists():
            raise ValidationError('This username is already taken.')

        return username



    def clean_password(self):
        password = self.cleaned_data.get('password')

        if len(password) < 8:
            raise ValidationError(
                'Password must be at least 8 characters long'
            )

        return password



    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password and password2 and password != password2:
            raise ValidationError('Passwords do not match.')

        return cleaned_data