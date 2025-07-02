from django import forms
from .models import SleepSession

class SleepSessionForm(forms.ModelForm):
    class Meta:
        model = SleepSession
        fields = ['start_time', 'end_time', 'note']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
