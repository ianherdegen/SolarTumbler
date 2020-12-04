from django.forms import ModelForm
from django import forms
from SolarTumbler.models import Group


# Create the form class.
class GroupForm(ModelForm):
    class Meta:
        model = Group
        fields = '__all__'

class CommentForm(forms.Form):
    comment = forms.CharField(required=True, max_length=500, min_length=3, strip=True)