from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()

class Review(models.Model):
    SENTIMENT_CHOICES = [
        ('positive', 'Positive'),
        ('negative', 'Negative'),
        ('neutral', 'Neutral'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField()
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    sentiment = models.CharField(max_length=8, choices=SENTIMENT_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    location_name = models.CharField(max_length=255, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    is_public = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'

    def __str__(self):
        return f"Review by {self.user.username} ({self.get_sentiment_display()})"

    def save(self, *args, **kwargs):
        # Auto-detect sentiment if not provided
        if not self.sentiment:
            self.sentiment = self.analyze_sentiment()
        super().save(*args, **kwargs)

    def analyze_sentiment(self):
        """
        Basic sentiment analysis based on rating
        Can be replaced with more advanced NLP analysis
        """
        if self.rating >= 4:
            return 'positive'
        elif self.rating <= 2:
            return 'negative'
        return 'neutral'
