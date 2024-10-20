from django import forms
from inventory_app.models import InventoryItem, Category

class InventoryItemForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label="Select a category")

    class Meta:
        model = InventoryItem
        fields = ['name', 'description', 'quantity', 'price', 'category']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }