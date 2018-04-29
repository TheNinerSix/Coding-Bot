from django import forms

class studentMenuForm(forms.Form):
	input = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'id':'commandLine','autofocus':'autofocus','autocomplete':'off'}))