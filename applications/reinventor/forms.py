from django import forms

from applications.account.models import Comuna, Pais, Region, Reinventor, WithdrawalRequestReinventor
from applications.reinventor.models import Company

from django.contrib.auth.forms import User

from reinventa.utils import validarRut



class UserForm(forms.ModelForm):

    tags_input_general = {
        'class': 'form-control',
        'autocomplete': 'off'
    }

    tags_input_readonly = {
        'class': 'form-control',
        'autocomplete': 'off',
        'readonly': 'readonly'
    }

    tags_input_select = {
        'class': 'form-control',
    }

    username = forms.CharField(label="Usuario",
                               widget=forms.TextInput(attrs=tags_input_general), help_text="debe ser el rut", required=True)
    first_name = forms.CharField(label="Nombres",
                                 widget=forms.TextInput(attrs=tags_input_general), required=True)
    last_name = forms.CharField(label="Apellidos",
                                widget=forms.TextInput(attrs=tags_input_general), required=True)
    email = forms.EmailField(label="Email",
                             widget=forms.TextInput(attrs=tags_input_general), required=True)
    password = forms.CharField(label="Contraseña",
                               widget=forms.PasswordInput(attrs=tags_input_general), required=False)

    def clean_username(self):
        data = self.cleaned_data["username"]

        if not validarRut(data):
            self.add_error('username', "El rut no es valido")
        return data

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password',
        ]


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
    co_latitude = forms.CharField(label="Latitude", widget=forms.TextInput(
        attrs=tags_input_general), required=False)
    co_longitude = forms.CharField(label="Longitude", widget=forms.TextInput(
        attrs=tags_input_general), required=False)
    
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
            'co_logo',
            'co_latitude',
            'co_longitude'
        ]


class WithdrawalRequestReinventorForm(forms.ModelForm):

    tags_input_general = {
        'class': 'form-control',
        'autocomplete': 'off'
    }

    tags_input_date = {
        "class": "form-control",
    }

    wrr_date = forms.DateField(input_formats=["%Y-%m-%d"], label="El retiro lo solicito para el día:",
                                    widget=forms.DateInput(format="%Y-%m-%d",
                                                           attrs=tags_input_date), required=True)
    wrr_quantityliters = forms.FloatField(label="Litros para retirar", widget=forms.TextInput(
        attrs=tags_input_general), required=True)
    
    class Meta:
        model = WithdrawalRequestReinventor
        fields = [
            'wrr_date',
            'wrr_quantityliters'
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
    
    re_latitude = forms.CharField(label="Latitude", widget=forms.TextInput(
        attrs=tags_input_general), required=False)
    re_longitude = forms.CharField(label="Longitude", widget=forms.TextInput(
        attrs=tags_input_general), required=False)

    class Meta:
        model = Reinventor
        fields = [
            're_nameentity',
            're_namereinventor',
            're_address',
            'pais',
            'region',
            'comuna',
            're_latitude',
            're_longitude'
        ]


class ReinventorLogoForm(forms.ModelForm):

    tags_input_file = {
        'class': 'form-control-file'
    }

    re_logo  = forms.ImageField(label="Logo Empresa", widget=forms.FileInput(
        attrs=tags_input_file), help_text=" Formatos .jpg|.png|.gif|.jpeg", required=True)
    
    class Meta:
        model = Reinventor
        fields = [
            're_logo'
        ]