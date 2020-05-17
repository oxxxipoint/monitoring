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
    zero = '0'
    one = '0.25'
    two = '0.5'
    three = '0.75'
    four = '1.0'

    VALUES = [(zero, 0),
              (one, 0.25),
              (two, 0.5),
              (three, 0.75),
              (four, 1.0)]

    value = forms.ChoiceField(label='Оценка', choices=VALUES,
                              initial=0,
                              widget=forms.RadioSelect)

    class Meta:
        model = DictObj
        exclude = ('container', 'key')

    def __init__(self, *args, **kwargs):
        super(DictObjForm, self).__init__(*args, **kwargs)
        self.fields['criteria'].widget.attrs.update({'class': 'input__style'})
        self.fields['value'].widget.attrs.update({'class': 'select__style'})


class CriteriaForm(forms.ModelForm):
    class Meta:
        model = Criteria
        fields = ('criteria_name', 'criteria_value')

    def __init__(self, *args, **kwargs):
        super(CriteriaForm, self).__init__(*args, **kwargs)
        self.fields['criteria_name'].widget.attrs.update({'class': 'input__style'})
        self.fields['criteria_value'].widget.attrs.update({'class': 'input__style'})
