from django import forms

from .models import Photo, Ticket, Review


class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['image', 'caption']


class TicketForm(forms.ModelForm):

    class Meta:
        model = Ticket
        fields = ['title', 'description']

    def save(self, commit=True, user=None):
        """Sauvegarde le ticket et la photo associée"""
        ticket = super().save(commit=False)
        if user:
            ticket.user = user  # Associe l'utilisateur connecté

        image_file = self.cleaned_data.get('image')
        if image_file:
            # Créer une instance de Photo et l'associer à l'utilisateur
            photo = Photo.objects.create(
                image=image_file,
                uploader=user
            )
            ticket.image = photo  # Associe l'instance de Photo au Ticket

        if commit:
            ticket.save()  # Sauvegarde finale

        return ticket


class DeleteTicketForm(forms.Form):
    delete_ticket = forms.BooleanField(widget=forms.HiddenInput, initial=True)


class ReviewForm(forms.ModelForm):
    RATING_CHOICES = [
        ('1', '1 ⭐ '),
        ('2', '2 ⭐⭐ '),
        ('3', '3 ⭐⭐⭐ '),
        ('4', '4 ⭐⭐⭐⭐'),
        ('5', '5 ⭐⭐⭐⭐⭐ ')
    ]

    rating = forms.ChoiceField(
        choices=RATING_CHOICES,
        widget=forms.RadioSelect,
        label='note'
    )

    class Meta:
        model = Review
        fields = ['headline', 'body', 'rating']
