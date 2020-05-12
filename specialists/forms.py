from django import forms

from .models import Specialist, Dict, DictObj, Criteria


class SpecialistForm(forms.ModelForm):
    class Meta:
        model = Specialist
        exclude = ('main_estim',)

    def __init__(self, *args, **kwargs):
        super(SpecialistForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'input__style'})
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
        exclude = ('container', 'key')
        fields = ('criteria', 'value')


class CriteriaForm(forms.ModelForm):
    class Meta:
        model = Criteria
        fields = ('criteria_name', 'criteria_value')

# class EstimForm(forms.ModelForm):
#     class Meta:
#         model = Estim
#         fields = ('key', 'value')
