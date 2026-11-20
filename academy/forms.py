from django import forms
from .models import ContactMessage


class ContactMessageForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ["full_name", "telegram_or_phone", "email", "subject", "message"]
        widgets = {
            "full_name": forms.TextInput(
                attrs={
                    "placeholder": "مثلاً: سارا محمدی",
                    "class": "form-input",
                }
            ),
            "telegram_or_phone": forms.TextInput(
                attrs={
                    "placeholder": "مثلاً: @username یا ۰۹۱۲...",
                    "class": "form-input",
                    "dir": "ltr",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "placeholder": "example@email.com (اختیاری)",
                    "class": "form-input",
                    "dir": "ltr",
                }
            ),
            "subject": forms.TextInput(
                attrs={
                    "placeholder": "مشاوره تعیین سطح، سفارش جزوه، کلاس خصوصی...",
                    "class": "form-input",
                }
            ),
            "message": forms.Textarea(
                attrs={
                    "rows": 5,
                    "placeholder": "پیام یا سوال خود را اینجا بنویسید...",
                    "class": "form-input",
                }
            ),
        }
