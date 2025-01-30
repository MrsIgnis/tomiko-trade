from django import forms
from django.core.validators import RegexValidator
from .models import Feedback


class FeedbackForm(forms.ModelForm):
    name = forms.CharField(
        label='Имя',
        max_length=20,
        required=True,
        validators=[RegexValidator(
            regex='^[a-zA-Zа-яА-ЯёЁ\s]+$',
            message='Имя должно содержать только буквы и пробелы'
        )],
        widget=forms.TextInput(attrs={
            'id': "id_name",
            'name': "name",
            'placeholder': "Введите имя",
            'title': "Имя должно содержать только буквы и пробелы.",
            'maxlength': "20",
            'required aria - describedby': "id_name_helptext",
            'pattern': "[a-zA-Zа-яА-ЯёЁ\s]+"
        })
    )

    phone_number = forms.CharField(
        label='Телефон',
        max_length=16,
        validators=[RegexValidator(
            regex='^\+7 [0-6,9]\d{2} \d{3} \d{2} \d{2}$',
            message='Номер должен быть в формате +7XXXXXXXXXX'
        )],
        widget=forms.TextInput(attrs={
            'id': "id_phone_number",
            'name': "phone_number",
            'placeholder': '+7',
            'title': "Формат: '+7 999 999 99 99' и номер не должен начинаться с 8 или 7 после кода +7",
            'maxlength': '16',
            'required aria - describedby': "id_phone_number_helptext",
            'pattern': '^\+7 [0-6,9]\d{2} \d{3} \d{2} \d{2}$'
        })
    )

    message = forms.CharField(
        label='Уточните свой вопрос',
        max_length=200,
        widget=forms.Textarea(attrs={
            'id': "id_message",
            'name': "message",
            'placeholder': 'Введите текст сообщения, укажите страну, марку и год машины.',
            'maxlength': '200',
            'cols': '40',
            'rows': '10'
        })
    )

    privacy_policy_confirm = forms.BooleanField(
        label='С <span class="confeditional_form">правилами политики конфиденциальности</span> ознакомлён',
        required=True,
        widget=forms.CheckboxInput(attrs={
            'id': "id_privacy_policy_confirm",
            'class': "checkbox",
            'checked': ''
        })
    )

    class Meta:
        model = Feedback
        fields = ['name', 'phone_number', 'message', 'privacy_policy_confirm']