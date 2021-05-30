from django.forms import ModelForm, TextInput, Textarea, DateTimeInput
from django import forms
from udachi.models import Otzivi, Bronirovanie, Zakaz
import datetime

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]


class CartAddBludaForm(forms.Form):
    quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES, coerce=int)
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)


class OstavitOtzivForm(ModelForm):
    class Meta:
        model = Otzivi
        fields = ['avtor', 'otziv', 'telephone_avtora']

        widgets = {"avtor": TextInput(attrs={
            'class': 'form-control', 'placeholder': 'Автор'}),
            "otziv": Textarea(attrs={
                'class': 'form-control', 'placeholder': 'Текст отзыва'}),
            "telephone_avtora": TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Номер телефона'}),
        }


class BronirovanieForm(ModelForm):
    class Meta:
        model = Bronirovanie
        fields = ['data', 'telephone', 'fio', 'kolvo_gostei']

        widgets = {"data": DateTimeInput(attrs={
            'class': 'form-control', 'placeholder': 'Желаемая дата и время', 'data-mask': '0000-00-00 00:00:00'}),
            "telephone": TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Номер телефона для подтверждения',
                'data-mask': '+7-000-000-00-00'}),
            "fio": TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Как можно к вам обращаться?'}),
            "kolvo_gostei": TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Укажите количество гостей'}),

        }

class ZakazCreateForm(ModelForm):
    class Meta:
        model = Zakaz
        fields = ['sposob_otdachi', 'fio', 'telephone', 'email', 'adres', 'bronirovanie']


        widgets = {
            "sposob_otdachi": TextInput(attrs={
                'class': 'form-control'}),
            "fio": TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Как можно к вам обращаться?'}),
            "telephone": TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Номер телефона для подтверждения',
                'data-mask': '+7-000-000-00-00'}),
            "email": TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Укажите адрес почты'}),
            "adres": TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Укажите адрес при доставке'}),
            "bronirovanie": TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Укажите номер брони при бронировании'}),

        }

