from django import forms
from .models import PresenceLog


class PresenceLogForm(forms.ModelForm):
    class Meta:
        model = PresenceLog
        fields = ["date", "type", "heure"]

        widgets = {
            "date": forms.DateInput(attrs={"type": "date", "class": "input input-bordered w-full"}),
            "heure": forms.TimeInput(attrs={"type": "time", "class": "input input-bordered w-full"}),
            "type": forms.Select(attrs={"class": "select select-bordered w-full"}),
        }