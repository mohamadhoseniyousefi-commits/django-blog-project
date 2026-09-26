from django import forms
from django.core.validators import ValidationError
from .models import Messages


class ContactForm(forms.Form):
    # select_year_birthday=['2021','2022','2023','2024','2025','2026']
    # favorite_color=[
    #     ('blue','blue'),
    #     ('red','red'),
    #     ('green','green'),
    # ]

    text = forms.CharField(max_length=10, label='yor message')
    name = forms.CharField(max_length=10, label='your name')
    # birthday = forms.DateField(label='birthday',widget=forms.SelectDateWidget(years=select_year_birthday))
    # favorite_color=forms.ChoiceField(label='favorite color',widget=forms.CheckboxSelectMultiple(),choices=favorite_color)
    skills = forms.ChoiceField(choices=[('py', 'Python'), ('dj', 'Django')], widget=forms.CheckboxSelectMultiple())

    def clean(self):
        text = self.cleaned_data.get('text')
        name = self.cleaned_data.get('name')
        if text == name:
            raise ValidationError('Your name is same text')

    def clean_text(self):
        text = self.cleaned_data.get('text')
        if 'a' in text:
            raise ValidationError('Your message has a')
        return text


class Message_form(forms.ModelForm):
    class Meta:
        model = Messages
        exclude = ('user',)

        widgets = {
        'title': forms.TextInput(attrs={
            'class': 'form-control rounded-4',
            'placeholder': 'title'
        }),

        'email': forms.EmailInput(attrs={
            'class': 'form-control rounded-4',
            'placeholder': 'Email Address'
        }),

        'text': forms.Textarea(attrs={
            'class': 'form-control rounded-4',
            'placeholder': 'Write your message...',
            'rows': 7
        }),
    }
