# profiles/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import UserProfile
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm


class CustomUserCreationForm(UserCreationForm):

    is_admin = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(
            attrs={'class': 'form-check-input mt-2 ms-4 p-3'}),



    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name',
                  'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_admin = self.cleaned_data['is_admin']

        if commit:
            user.is_active = False
            user.save()
            UserProfile.objects.create(user=user, is_admin=user.is_admin)

        return user

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            if field != 'is_admin':
                self.fields[field].widget.attrs.update({
                    'class': (
                        'form-control'
                        ' bg-light'
                        ' text-dark'
                        ' border'
                        ' rounded'
                        ' py-3 px-4'
                        ' focus:outline-none'
                        ' focus:bg-white'
                        'w-50'

                    )
                })


class CustomUserUpdateForm(UserChangeForm):

    is_admin = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(
            attrs={'class': 'form-check-input mt-2 ms-4 p-3'}),



    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name',
                  'email', 'is_admin']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            if field != 'is_admin':
                self.fields[field].widget.attrs.update({
                    'class': (
                        'form-control'
                        ' bg-light'
                        ' text-dark'
                        ' border'
                        ' rounded'
                        ' py-3 px-4'
                        ' focus:outline-none'
                        ' focus:bg-white'

                        'w-50'

                    )
                })


class CustomLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': (
                    'form-control'
                    ' bg-light'
                    ' text-dark'
                    ' border'
                    ' rounded'
                    ' py-3 px-4'
                    ' focus:outline-none'
                    ' focus:bg-white'

                    ' w-75'
                )
            })
