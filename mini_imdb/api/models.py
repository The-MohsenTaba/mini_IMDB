from django.db import models
from django.contrib.auth.models import AbstractUser
from mongoengine import Document,StringField,IntField,FloatField,EnumField,ReferenceField,ListField
from enum import Enum
from django.core.exceptions import ValidationError


# SQL Models ( app mainly works with this data )
class Person(models.Model):
    first_name = models.CharField(null=False,max_length=50)
    last_name = models.CharField(null=False,max_length=50)
    def __str__(self):
        return self.first_name + " " + self. last_name
    

class Movie (models.Model):
    class GenereChoices(models.TextChoices):
        ACTION="Action",
        COMEDY="Comedy"
        DRAMA="Drama"
        HORROR="Horror"
        ROMANCE="Romance"
        BIOGRAPHY="Biography"
        SCIFI="Sci-fi"
        THRILLER="Thriller"
    title= models.CharField(null=False,max_length=50)
    year = models.IntegerField(null=True)
    genere= models.CharField(null=True,choices=GenereChoices,max_length=50)
    average_rating=models.FloatField(default=0)
    rating_count=models.PositiveIntegerField(default=0)
    directors = models.ManyToManyField(Person,related_name="directors")
    actors = models.ManyToManyField(Person,related_name="actors")

    def clean(self):
        if self.genere not in self.GenereChoices.values:
            raise ValidationError("invalid genere!")
        
        if ((self.average_rating > 10) or (self.average_rating<0)) :
            raise ValidationError("average rating out of range ! 0-10")
        
        if self.rating_count < 0 : 
            raise ValidationError(" rating counts cannot be negative !")
        



    def update_rating_stats(self):
        from django.db.models import Avg,Count
        stats = self.vote_set.aggregate(
            average=Avg('rating'),
            count=Count('id')
        )
        self.average_rating = stats['average'] or 0
        self.rating_count = stats['count'] or 0
        self.save(update_fields=['average_rating', 'rating_count'])

    def save(self,*args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

class User(AbstractUser): # This SQL data model will use for both SQLite and MongoDB Databases
    pass
    def __str__(self):
        return self.username
    


class Vote(models.Model):
    rating = models.DecimalField(max_digits=2,decimal_places=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie= models.ForeignKey(Movie,on_delete=models.CASCADE)

    def clean(self):
        if self.rating > 10 or self.rating<0:
            raise ValidationError("rating is out of range !(0-10)")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
        self.movie.update_rating_stats()
    
    def delete(self, *args, **kwargs):
        movie = self.movie
        super().delete(*args, **kwargs)
        movie.update_rating_stats()






# MongoDB documents

class MongoPerson(Document):
    first_name = StringField(required = True , max_length= 50)
    last_name = StringField(required = True , max_length= 50)
    def __str__(self):
        return self.first_name +" "+ self.last_name
    
class GenreEnum(Enum):
    ACTION="Action"
    COMEDY="Comedy"
    DRAMA="Drama"
    HORROR="Horror"
    ROMANCE="Romance"
    BIOGRAPHY="Biography"
    SCIFI="Sci-fi"
    THRILLER="Thriller"

class MongoMovie(Document):
    title = StringField(required=True, max_length=100)
    year = IntField()
    genere = EnumField(GenreEnum)
    rating_count = IntField(default =0)
    average_rating = FloatField(default =0)
    directors = ListField(ReferenceField(MongoPerson))
    actors = ListField(ReferenceField(MongoPerson))

    def __str__(self):
        return f"{self.title} ({self.year}) - {self.average_rating}"
    
    
    def update_rating_stats(self):
        ratings = MongoVote.objects(movie = self)
        if ratings:
            count = ratings.count()
            rates = sum([float(r.rating) for r in ratings])
            self.rating_count = count
            self.average_rating = round(rates/count,1)

        else:
            self.rating_count= 0
            self.average_rating = 0
        self.save()

class MongoVote(Document):
    user = StringField(required = True , max_length=50)
    movie = ReferenceField(MongoMovie, required = True)
    rating = FloatField(precision = 1 , min_value=0 , max_value= 5 , required = True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.movie.update_rating_stats()

    def delete(self , *args, **kwargs):
        movie = self.movie
        super().delete(*args, **kwargs)
        movie.update_rating_stats()

        
