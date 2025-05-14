from django import forms
from .models import Review
from django.core.validators import MinValueValidator, MaxValueValidator

class ReviewForm(forms.ModelForm):
    rating = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'type': 'range',
            'min': '1',
            'max': '5',
            'step': '1',
            'class': 'form-range',
            'id': 'ratingSlider'
        }),
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )

    class Meta:
        model = Review
        fields = ['text', 'rating', 'location_name', 'latitude', 'longitude', 'is_public']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Share your experience...'
            }),
            'location_name': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'locationInput',
                'placeholder': 'Location name'
            }),
            'latitude': forms.HiddenInput(),
            'longitude': forms.HiddenInput(),
            'is_public': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.user:
            instance.user = self.user
        if commit:
            instance.save()
        return instance
