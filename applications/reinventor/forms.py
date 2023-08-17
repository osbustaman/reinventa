from django import forms

from applications.account.models import Comuna, Pais, Region, Reinventor
from applications.reinventor.models import Company
from reinventa.utils import validarRut


class CompanyForm(forms.ModelForm):

    tags_input_general = {
        'class': 'form-control',
        'autocomplete': 'off'
    }

    tags_input_file = {
        'class': 'form-control-file'
    }

    tags_input_select = {
        'class': 'form-control',
    }

    tags_input_select2 = {
        'class': 'form-control select2-show-search',
    }

    co_name = forms.CharField(label="Nombre empresa", widget=forms.TextInput(
        attrs=tags_input_general), required=True)
    co_address = forms.CharField(label="Dirección", widget=forms.TextInput(
        attrs=tags_input_general), help_text="ej: calle siempre viva 1010", required=True)
    pais = forms.ModelChoiceField(label="País", required=True,
                                    queryset=Pais.objects.all(), widget=forms.Select(attrs=tags_input_select2 ))
    region = forms.ModelChoiceField(label="Región", required=True,
                                    queryset=Region.objects.all(), widget=forms.Select(attrs=tags_input_select2 ))
    comuna = forms.ModelChoiceField(label="Comuna", required=True,
                                    queryset=Comuna.objects.all(), widget=forms.Select(attrs=tags_input_select2 ))
    co_logo  = forms.ImageField(label="Logo Empresa", widget=forms.FileInput(
        attrs=tags_input_file), help_text=" Formatos .jpg|.png|.gif|.jpeg", required=False)

    class Meta:
        model = Company
        fields = [
            'co_name',
            'co_address',
            'pais',
            'region',
            'comuna',
            'co_logo'
        ]


class ReinventorForm(forms.ModelForm):

    tags_input_general = {
        'class': 'form-control',
        'autocomplete': 'off'
    }

    tags_input_select = {
        'class': 'form-control',
    }

    tags_input_date = {
        "class": "form-control fc-datepicker",
        "placeholder": "DD-MM-YYYY",
    }

    tags_input_file = {
        'class': 'form-control-file'
    }

    tags_input_select2 = {
        'class': 'form-control select2-show-search',
    }

    re_nameentity = forms.CharField(label="Nombre empresa", widget=forms.TextInput(
        attrs=tags_input_general), required=True)
    re_namereinventor = forms.CharField(label="Nombre representante", widget=forms.TextInput(
        attrs=tags_input_general), required=True)
    re_address = forms.CharField(label="Dirección", widget=forms.TextInput(
        attrs=tags_input_general), help_text="ej: calle siempre viva 1010", required=True)
    pais = forms.ModelChoiceField(label="País", required=True,
                                    queryset=Pais.objects.all(), widget=forms.Select(attrs=tags_input_select2 ))
    region = forms.ModelChoiceField(label="Región", required=True,
                                    queryset=Region.objects.all(), widget=forms.Select(attrs=tags_input_select2 ))
    comuna = forms.ModelChoiceField(label="Comuna", required=True,
                                    queryset=Comuna.objects.all(), widget=forms.Select(attrs=tags_input_select2 ))
    re_logo  = forms.ImageField(label="Logo Empresa", widget=forms.FileInput(
        attrs=tags_input_file), help_text=" Formatos .jpg|.png|.gif|.jpeg", required=False)
    

    class Meta:
        model = Reinventor
        fields = [
            're_nameentity',
            're_namereinventor',
            're_address',
            'pais',
            'region',
            'comuna',
            're_logo'
        ]