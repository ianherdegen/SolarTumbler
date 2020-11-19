from django.forms import ModelForm
from django import forms
from SolarTumbler.models import Item


# Create the form class.
class ItemForm(ModelForm):
    class Meta:
        model = Item
        fields = '__all__'

class CommentForm(forms.Form):
    comment = forms.CharField(required=True, max_length=500, min_length=3, strip=True)