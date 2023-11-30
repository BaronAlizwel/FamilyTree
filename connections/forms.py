from django import forms
from .models import Connection, ConnectionRequest


class ConnectionForm(forms.ModelForm):
    class Meta:
        model = Connection
        fields = ['from_user', 'to_user', 'relationship_type', 'relationship_name']
        widgets = {
            'from_user': forms.Select(attrs={'class': 'form-control'}),
            'to_user': forms.Select(attrs={'class': 'form-control'}),
            'relationship_type': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'from_user': 'From User',
            'to_user': 'To User',
            'relationship_type': 'Relationship Type',
        }
        

class AcceptConnectionRequestForm(forms.ModelForm):
    class Meta:
        model = ConnectionRequest
        fields = []
        widgets = {'status': forms.HiddenInput()}
        

class RejectConnectionRequestForm(forms.ModelForm):
    class Meta:
        model = ConnectionRequest
        fields = []
        widgets = {'status': forms.HiddenInput()}
