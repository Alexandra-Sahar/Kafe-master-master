from django.forms import ModelForm

from udachi.models import Otzivi


class OstavitOtzivForm(ModelForm):
    class Meta:
        model = Otzivi
        fields = ['avtor', 'otziv', 'telephone_avtora']

