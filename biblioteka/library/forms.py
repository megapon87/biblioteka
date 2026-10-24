from django import forms
from django.contrib.auth.models import User


class RegisterForm(forms.Form):
    
    username = forms.CharField(max_length=50, label="Логін")
    email = forms.EmailField(label="Email", required=False)
    password1 = forms.CharField(widget=forms.PasswordInput(), label="Пароль")
    password2 = forms.CharField(widget=forms.PasswordInput(), label="Повторіть пароль")

    def clean_username(self):
        username = self.cleaned_data["username"]
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Такий логін вже зайнятий")
        return username

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get("password1")
        p2 = cleaned_data.get("password2")
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("Паролі не співпадають")
        return cleaned_data


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50, label="Логін")
    password = forms.CharField(widget=forms.PasswordInput(), label="Пароль")
