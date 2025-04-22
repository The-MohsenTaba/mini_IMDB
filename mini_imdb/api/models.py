from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class Movie (models.Model):
    title= models.CharField(null=False,max_length=50)
    year = models.IntegerField(null=True)
    average_rating=models.FloatField(default=0)
    rating_count=models.PositiveIntegerField(default=0)
    def update_rating_stats(self):
        from django.db.models import Avg,Count
        stats = self.vote_set.aggregate(
            average=Avg('rating'),
            count=Count('id')
        )
        self.average_rating = stats['average'] or 0
        self.rating_count = stats['count'] or 0
        self.save(update_fields=['average_rating', 'rating_count'])

class User(AbstractUser):
    pass
    def __str__(self):
        return self.username

class Vote(models.Model):
    rating = models.DecimalField(max_digits=2,decimal_places=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie= models.ForeignKey(Movie,on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.movie.update_rating_stats()
    
    def delete(self, *args, **kwargs):
        movie = self.movie
        super().delete(*args, **kwargs)
        movie.update_rating_stats()

# we will add genre later . 