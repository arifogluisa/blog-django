from django import forms
from .models import Comment, Contact
from django.utils.translation import gettext_lazy as _


class CommentForm(forms.ModelForm):
    text = forms.CharField(
        required=True,
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'placeholder': 'Şərhinizi yazın...',
                'rows': '3',
            },
        )
    )

    class Meta:
        model = Comment
        fields = ("text",)


class ContactForm(forms.ModelForm):
    full_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'contact-form-txt',
        'placeholder': _('Ad Soyad')
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'contact-form-txt',
        'placeholder': _('Email')
    }))
    message = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'contact-form-textarea',
        'placeholder': _('Mətin')
    }))

    class Meta:
        model = Contact
        fields = ['full_name', 'email', 'message']
