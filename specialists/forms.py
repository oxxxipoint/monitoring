from django import forms

from .models import Specialist, Dict, DictObj


class SpecialistForm(forms.ModelForm):
    class Meta:
        model = Specialist
        exclude = ()

    def __init__(self, *args, **kwargs):
        super(SpecialistForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class' : 'input__style'})
        self.fields['surname'].widget.attrs.update({'class': 'input__style'})
        self.fields['patronymic'].widget.attrs.update({'class': 'input__style'})
        self.fields['birth'].widget.attrs.update({'class': 'input__style'})


class DictForm(forms.ModelForm):
    class Meta:
        model = Dict
        fields = ('spec', 'dictName')


class DictObjForm(forms.ModelForm):
    class Meta:
        model = DictObj
        fields = ('container', 'key', 'value')
