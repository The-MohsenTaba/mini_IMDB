from django.test import TestCase
from api.models import Movie,Vote
from django.core.exceptions import ValidationError




class MovieModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.movie = Movie(title='something',year = 1111,genere="action")

    def test_movie_genere_entry(self):
        """ test if only valid generes can be used """
        self.movie.genere="invalid genere!"
        with self.assertRaises(ValidationError):
            self.movie.save()
    def test_negative_average_rating(self):
        self.movie.average_rating = -10
        with self.assertRaises(ValidationError):
            self.movie.save()
    def test_maximum_average_rating(self):
        self.movie.average_rating = 100
        with self.assertRaises(ValidationError):
            self.movie.save()
    def test_negative_raitng_count(self):
        self.movie.rating_count = -1
        with self.assertRaises(ValidationError):
            self.movie.save()


class VoteModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.vote = Vote(rating=10)
    def test_minimum_rating_value(self):
        self.vote.rating = -10
        with self.assertRaises(ValidationError):
            self.vote.save()
    def test_maximum_rating_value(self):
        self.vote.rating = 100
        with self.assertRaises(ValidationError):
            self.vote.save()