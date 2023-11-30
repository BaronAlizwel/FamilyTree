from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields
        

class CustomUserChangeForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['bio', 'location', 'birthdate', 'interests', 'hobbies', 'is_public']
        widgets = {
            'is_public': forms.CheckboxInput(),
        }
        

class UserSearchForm(forms.Form):
    username = forms.CharField(max_length=50, required=False)
    location = forms.CharField(max_length=100, required=False)
    bio = forms.CharField(max_length=500, required=False)
