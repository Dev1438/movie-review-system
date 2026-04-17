from django import forms
from .models import Movie

class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['title', 'description', 'genre', 'rating', 'poster']

    widgets = {
        'title': forms.TextInput(attrs={
            'class': 'form-control bg-black text-light border-secondary',
            'placeholder': 'Enter movie title'
        }),
        'description': forms.Textarea(attrs={
            'class': 'form-control bg-black text-light border-secondary',
            'rows': 4
        }),
        'genre': forms.Select(attrs={
            'class': 'form-select bg-black text-light border-secondary'
        }),
        'rating': forms.NumberInput(attrs={
            'class': 'form-control bg-black text-light border-secondary',
            'min': 1, 'max': 10, 'step': 0.1
        }),
        'poster': forms.ClearableFileInput(attrs={
            'class': 'form-control bg-black text-light border-secondary'
        }),
    }

    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        if rating < 1 or rating > 10:
            raise forms.ValidationError("Rating must be between 1 and 10.")
        return rating