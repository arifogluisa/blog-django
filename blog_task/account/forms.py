from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Account


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']


# for admin side
class AccountCreateForm(forms.ModelForm):
    """
        A form for creating new account.
        Includes all the required fields, plus a repeated password.
    """

    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput,
    )

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        instance = super().save(commit=False)

        instance.set_password(self.cleaned_data["password1"])
        if commit:
            instance.save()
        return instance
