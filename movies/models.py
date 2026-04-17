from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.


 
class Movie(models.Model):
        GENRE_CHOICES=[
            ('action', 'Action'),
            ('drama', 'Drama'),
            ('comedy', 'Comedy'),
            ('thriller', 'Thriller'),
            ('sci_fi', 'Sci-Fi'),
        ]
    
        title       = models.CharField(max_length=200)
        description = models.TextField()
        genre       = models.CharField(max_length=50, choices=GENRE_CHOICES)
        rating      = models.DecimalField(
            max_digits=3, decimal_places=1,
            validators=[MinValueValidator(1), MaxValueValidator(10)]
        )
        poster      = models.ImageField(upload_to='posters/')
        created_at  = models.DateTimeField(auto_now_add=True)

        def __str__(self):
            return self.title