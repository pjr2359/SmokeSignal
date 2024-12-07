from django import forms
from .models import Activity

class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ['strain_name', 'strain_type', 'rating', 'location', 'notes']
