from django import forms


from .models import Humm

from django.conf import settings


MAX_HUMM_LENGTH = settings.MAX_HUMM_LENGTH


class CreateHumm(forms.ModelForm):
    class Meta:
        model = Humm
        fields = ['content']

    def clean_content(self):
        content = self.cleaned_data.get("content")
        print(MAX_HUMM_LENGTH)
        if len(content) > MAX_HUMM_LENGTH:
            raise forms.ValidationError("This humm is too long")
        return content
