# encoding: utf-8

'''

@author: ZiqiLiu


@file: forms.py

@time: 2017/9/15 下午8:35

@desc:
'''
from django import forms
from .models import User, Preference


class UserCreationForm(forms.Form):
    username = forms.RegexField(
        max_length=128,
        regex=r'^[\w]{6,128}$',
        error_messages={
            'invalid': 'username should only contain letters, number, and "_", and must longer than 6 characters.',
            'required': 'username is empty'
        },
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Username....",
                   "id": "form-username"}),
        help_text="username must be 6-128 digits letters or numbers."
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Password....",
                   "id": "form-password"}),
        error_messages={
            'required': 'confirm password is empty'
        },
        help_text="password must be more than 6 characters."
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control",
                   "placeholder": "Confirm your Password....",
                   "id": "form-confirm-password"}),
        error_messages={
            'required': 'confirm password is empty'
        },
        help_text='must match the password above.'
    )
    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Email....",
                   "id": "form-email"}),
        error_messages={
            'invalid': 'invalid email!',
            'required': 'email is empty'}
    )
    first_name = forms.RegexField(
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "First name....",
                   "id": "form-fname"}),
        max_length=64,
        regex=r'^[a-zA-Z]+$',
        error_messages={
            'invalid': 'first name invalid.',
            'required': 'first name is empty'
        }
    )
    last_name = forms.RegexField(
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Last name....",
                   "id": "form-lname"}),
        max_length=64,
        regex=r'^[a-zA-Z]+$',
        error_messages={
            'invalid': 'last name invalid.',
            'required': 'last name is empty'
        }
    )
    nick_name = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control",
                   "placeholder": "Your nick name (optional)",
                   "id": "form-nickname"}),
        max_length=64,
        error_messages={
            'invalid': 'nick name invalid.',
        }, required=False
    )

    def clean(self):
        cleaned_data = super(UserCreationForm, self).clean()

        # Confirms that the two password fields match
        password1 = cleaned_data.get('password')
        password2 = cleaned_data.get('confirm_password')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords did not match.")

        # Generally return the cleaned data we got from our parent.
        return cleaned_data

    def clean_username(self):
        # check if there is duplicate username
        username = self.cleaned_data['username']
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError('duplicate username!')

    def clean_nick_name(self):
        nick_name = self.cleaned_data.get('nick_name').strip()
        if len(nick_name) == 0:
            nick_name = self.cleaned_data.get(
                'first_name') + ' ' + self.cleaned_data.get('last_name')
        return nick_name


class LoginForm(forms.Form):
    username = forms.CharField(
        error_messages={
            'required': 'username is empty'
        },
        widget=forms.TextInput(
            attrs={"class": "form-control",
                   "id": "form-username"}),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control",
                   "id": "form-password"}),
        error_messages={
            'required': 'password is empty'
        },
    )


class ProfileForm(forms.Form):
    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Email....",
                   "id": "form-email"}),
        error_messages={
            'invalid': 'invalid email!',
            'required': 'email is empty'}
    )
    first_name = forms.RegexField(
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "First name....",
                   "id": "form-fname"}),
        max_length=64,
        regex=r'^[a-zA-Z]+$',
        error_messages={
            'invalid': 'first name invalid.',
            'required': 'first name is empty'
        }
    )
    last_name = forms.RegexField(
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Last name....",
                   "id": "form-lname"}),
        max_length=64,
        regex=r'^[a-zA-Z]+$',
        error_messages={
            'invalid': 'last name invalid.',
            'required': 'last name is empty'
        }
    )
    nick_name = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control",
                   "placeholder": "Your nick name (optional)",
                   "id": "form-nickname"}),
        max_length=64,
        error_messages={
            'invalid': 'nick name invalid.',
            'required': 'last name is empty'
        }
    )

    img = forms.ImageField(label='profile image', required=False)


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Old Password....",
                   "id": "old-form-password"}),
        error_messages={
            'required': 'Old password is empty'
        },
        help_text="password must be more than 6 characters."
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "New Password....",
                   "id": "form-password"}),
        error_messages={
            'required': 'password is empty'
        },
        help_text="password must be more than 6 characters."
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control",
                   "placeholder": "Confirm your Password....",
                   "id": "form-confirm-password"}),
        error_messages={
            'required': 'confirm password is empty'
        },
        help_text='must match the password above.'
    )

    def clean(self):
        cleaned_data = super(ChangePasswordForm, self).clean()

        # Confirms that the two password fields match
        password1 = cleaned_data.get('password')
        password2 = cleaned_data.get('confirm_password')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords did not match.")

        # Generally return the cleaned data we got from our parent.
        return cleaned_data



class ResetPasswordForm(forms.Form):
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "New Password....",
                   "id": "form-password"}),
        error_messages={
            'required': 'password is empty'
        },
        help_text="password must be more than 6 characters."
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control",
                   "placeholder": "Confirm your Password....",
                   "id": "form-confirm-password"}),
        error_messages={
            'required': 'confirm password is empty'
        },
        help_text='must match the password above.'
    )

    def clean(self):
        cleaned_data = super(ResetPasswordForm, self).clean()

        # Confirms that the two password fields match
        password1 = cleaned_data.get('password')
        password2 = cleaned_data.get('confirm_password')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords did not match.")

        # Generally return the cleaned data we got from our parent.
        return cleaned_data

class ForgetPasswordForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control",
                   "placeholder": "Please enter your username",
                   "id": "form-username"}),
        error_messages={
            'required': 'You must provide your username'
        },
        help_text="Enter your username to help us identify your account"
    )

    def clean_username(self):
        # check if there is duplicate username
        username = self.cleaned_data['username']
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            raise forms.ValidationError('User non exist!')
        return username

class PreferenceForm(forms.ModelForm):
    class Meta:
        model = Preference
        fields = '__all__'

