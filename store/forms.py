from django import forms
from django.forms import ModelForm
from .models import Reviews

class formReviews(forms.ModelForm):
    class Meta:
        model= Reviews
        fields= ["description",'ratings']
