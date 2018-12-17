from django import forms
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db import models

from django.http import request


class RegisterForm(forms.ModelForm):
    username = forms.CharField(label='Username', max_length=20)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email','username', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get("email")
        checkemail = User.objects.filter(email__iexact=email)
        if checkemail.exists():
            raise forms.ValidationError("Email already exists")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Password does not match")
        return password1

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class Login(forms.Form):
    username = forms.CharField(label="Username")
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

    def clean(self):
        uname = self.cleaned_data.get("username")
        pass1 = self.cleaned_data.get("password")
        user = authenticate(request, username=uname, password=pass1)
        if user is None:
            raise forms.ValidationError("Invalid Username / Password")
        return super(Login, self).clean()

class BlogEntries(models.Model):
    title = models.CharField(max_length=60)
    blog_body = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    datetimeofentry = models.DateTimeField(auto_now=True)
    blogimage = models.ImageField(upload_to='myimages', blank=True, null=True)

    # def __str__(self):
    #     return self.title