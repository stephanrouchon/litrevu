from django import forms

from . import models

class PhotoForm(forms.ModelForm):
    class Meta:
        model = models.Photo
        fields = ['image','caption']

class TicketForm(forms.ModelForm):
    edit_ticket = forms.BooleanField(widget=forms.HiddenInput, initial=True)
    
    class Meta:
        model = models.Ticket
        fields = ['title', 'description']

class DeleteTicketForm(forms.Form):
    delete_ticket = forms.BooleanField(widget=forms.HiddenInput, initial=True)


class ReviewForm(forms.ModelForm):
    RATING_CHOICES = [
        ('1', '1 ⭐ '),
        ('2', '2 ⭐⭐ '),
        ('3', '3 ⭐⭐⭐ '),
        ('4', '4 ⭐ ⭐⭐⭐'),
        ('5', '5 ⭐⭐⭐⭐⭐ ')
    ]

    rating= forms.ChoiceField(
        choices=RATING_CHOICES,
        widget=forms.RadioSelect,
        label='note'
    )
    class Meta:
        model = models.Review
        fields= ['rating','headline','body']
