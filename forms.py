from django.forms import ModelForm
from SolarTumbler.models import Item


# Create the form class.
class ItemForm(ModelForm):
    class Meta:
        model = Item
        fields = '__all__'