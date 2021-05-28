from django.forms import ModelForm, TextInput, Textarea, DateTimeInput

from udachi.models import Otzivi, Bronirovanie


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
