# forms.py

from django import forms
from .models import InventoryItem

class InventoryItemForm(forms.ModelForm):
    class Meta:
        model = InventoryItem
        fields = ['name', 'quantity', 'image']


from django import forms
from .models import InventoryRequest

from django import forms
from .models import InventoryRequest, SportsCenter

class InventoryRequestForm(forms.ModelForm):
    class Meta:
        model = InventoryRequest
        fields = ['sports_center', 'item', 'new_item_name', 'quantity_requested']
        widgets = {
            'sports_center': forms.Select(attrs={'class': 'form-control'}),
            'item': forms.Select(attrs={'class': 'form-control'}),
            'new_item_name': forms.TextInput(attrs={'class': 'form-control'}),
            'quantity_requested': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        logged_in_trainer = kwargs.pop('trainer', None)
        super().__init__(*args, **kwargs)
        if logged_in_trainer:
            self.fields['trainer'].initial = logged_in_trainer




