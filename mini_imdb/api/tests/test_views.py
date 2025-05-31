from django.test import TestCase
from api.models import User,Movie
from django.core.exceptions import ValidationError
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

class TestAuthentication(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='user1',password ="test123")
        cls.data = {
            'username': 'user1',
            'password': 'test123'
        }

    def test_vote_action_authenticated(self):
        #first making a movie to submit a rating for it 
        movie = Movie(title='something',year = 1111,genere="Action")
        movie.save()
        # then call our login to get access tokens
        response=self.client.post(reverse('token_obtain_pair'), self.data, format ='json')
        self.assertEqual(response.status_code , 200 )
        token = response.data['access']
        # now test if view works fine 
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        url=reverse('movies-vote', kwargs={'pk':movie.pk})
        response = self.client.post(url, data={'rating':1},format='json')
        self.assertEqual(response.status_code, 201)

    # def test_update_vote_action_authenticated(self):
    #     pass
    def test_user_ratings_authenticated(self):
        # first call our login to get access tokens
        response=self.client.post(reverse('token_obtain_pair'), self.data, format ='json')
        self.assertEqual(response.status_code , 200 )
        token = response.data['access']
        # now test if view works fine 
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        # self.client.credentials(HTTP_AUTHORIZATION='JWT {0}'.format(token))
        response = self.client.get(reverse('my-ratings'), format= 'json')
        self.assertEqual(response.status_code, 200)
