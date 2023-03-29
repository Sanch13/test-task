from django import forms
from services.middleware import get_list_name_currencies


class DateRateForm(forms.Form):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    uid = forms.ChoiceField(choices=get_list_name_currencies(),
                            widget=forms.Select)
