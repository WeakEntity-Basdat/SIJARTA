from django import forms
from .models import Testimoni

class TestimoniForm(forms.ModelForm):
    class Meta:
        model = Testimoni
        fields = ['worker', 'rating', 'comment']
