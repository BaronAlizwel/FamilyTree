from django import forms
from .models import Message
from users.models import CustomUser


class MessageForm(forms.ModelForm):
    recipient = forms.ModelChoiceField(queryset=CustomUser.objects.all())
    subject = forms.CharField(max_length=200)

    class Meta:
        model = Message
        fields = ['recipient', 'subject', 'body']
