from django import forms

class ClockInForm(forms.Form):
    file = forms.FileField()