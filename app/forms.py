from django.forms.models import inlineformset_factory
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.models import Group
from django import forms
from .models import *

class UserAdminCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email',)

    def clean_confirm_password(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class UserAdminChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()
    class Meta:
        model = User
        fields = ('email', 'password', 'is_active', 'is_superuser')

    def clean_password(self):
        return self.initial["password"]

class SignUpForm(forms.ModelForm):
    travel_history = forms.CharField(widget=forms.Textarea(attrs={"rows":5}), required=False)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    cpassword = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['email','first_name','middle_name','last_name','suffix','sex','birthdate','address','province','city','contact_number','travel_history']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("email is taken")
        return email

    def clean_cpassword(self):
        password = self.cleaned_data.get("password")
        cpassword = self.cleaned_data.get("cpassword")
        if password != cpassword:
            raise forms.ValidationError("Passwords don't match")
        return cpassword

    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
            group = Group.objects.get(name='User') 
            group.user_set.add(user)
        return user

class ProfileForm(forms.ModelForm):
    travel_history = forms.CharField(required=False, widget=forms.Textarea(attrs={"rows":5}))
    image = forms.ImageField(widget=forms.FileInput, required=False)
    class Meta:
        model = User
        fields = ['first_name','middle_name','last_name','suffix','sex','birthdate','address','province','city','contact_number', 'image','travel_history']

class PlaceForm(forms.ModelForm):
    image = forms.ImageField(widget=forms.FileInput, required=False)
    class Meta:
        model = Place
        fields = ['place','image','address','province','city']

class CheckInForm(forms.ModelForm):
    class Meta:
        model = CheckIn
        fields = '__all__'