from django import forms

class ArtefactForm(forms.Form):
        artefactid = forms.CharField(label='Artefact Id:', max_length=300,widget=forms.TextInput(attrs={'size':50}))