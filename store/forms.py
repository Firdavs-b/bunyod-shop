# store/forms.py
from django import forms

class ProfitDateForm(forms.Form):
    DATE_CHOICES = [
        ('day', 'Рӯз'),
        ('month', 'Моҳ'),
    ]
    date_type = forms.ChoiceField(choices=DATE_CHOICES, label='Намуди сана')
    selected_date = forms.DateField(
        label='Сана', 
        widget=forms.DateInput(attrs={'type': 'date'})
    )
