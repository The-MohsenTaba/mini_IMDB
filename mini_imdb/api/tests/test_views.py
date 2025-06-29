from api.models import User,Movie
from django.urls import reverse
from rest_framework.test import APITestCase

class TestAuthentication(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='user1',password ="test123")
        cls.data = {
            'username': 'user1',
            'password': 'test123'
        }

    def create_movie(self):
        """ a helper method builds movie sample for tests """
        movie = Movie(title='something',year = 1111,genere="Action")
        movie.save()
        return movie
    
    def authenticate(self):
        """ a helper method that authenticate and get access tokens , set credentials for requests """
        response=self.client.post(reverse('token_obtain_pair'), self.data, format ='json')
        self.assertEqual(response.status_code , 200 )
        token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')


    def test_vote_action_authenticated(self):
        """ test rating system responses """
        #first making a movie to submit a rating for it 
        movie=self.create_movie()
        # then we check our unauthentication error works fine 
        url=reverse('movies-vote', kwargs={'pk':movie.pk})
        response = self.client.post(url, data={'rating':1},format='json')
        self.assertEqual(response.status_code, 401)
        
        # and testing app authenticated
        self.authenticate()
        response = self.client.post(url, data={'rating':1},format='json')
        self.assertEqual(response.status_code, 201)
    def test_update_vote_action_authenticated(self):
        """ test updating ratings system """
        #first making a movie to submit a rating for it 
        movie=self.create_movie()
        # then we check our unauthentication error works fine 
        url=reverse('movies-vote', kwargs={'pk':movie.pk})
        response = self.client.post(url, data={'rating':1},format='json')
        self.assertEqual(response.status_code, 401)

        # then we test authenticated rating post 
        self.authenticate()
        response = self.client.post(url, data={'rating':1},format='json')
        self.assertEqual(response.status_code, 201)
        
        # and finally authenticated update 
        url=reverse('movies-update-vote',kwargs={'pk':movie.pk})
        response = self.client.put(url, data={'rating':4},format='json')
        self.assertEqual(response.status_code, 200)

    def test_user_ratings_authenticated(self):
        """ test authentication errors for user ratings """
        # unauthentication error sending 
        response = self.client.get(reverse('my-ratings'), format= 'json')
        self.assertEqual(response.status_code, 401)

        # works fine authenticated
        self.authenticate()
        response = self.client.get(reverse('my-ratings'), format= 'json')
        self.assertEqual(response.status_code, 200)

class TestQuerysets(APITestCase):

    def create_user(self,n):
        """ a helper method builds user samples for tests """
        for i in range(n):
            User.objects.create_user(username=f'username{i}',password='test123')

    def create_movies(self,n):
        """ a helper method builds movie samples for tests """
        for i in range (n):
            movie = Movie(title=f'something{i}',year = 1111,genere="Action")
            movie.save()

    def test_list_of_movies(self):
        """ test if created movies are shown in movies list"""
        count=5
        self.create_movies(count)
        response= self.client.get(reverse('movies-list'),format='json')
        self.assertEqual(len(response.data),count)

    def test_single_movie_return(self):
        """ test if created movie's detail page exists """
        self.create_movies(1)
        response= self.client.get(reverse('movies-detail',kwargs={'pk':1}),format='json')
        self.assertEqual(response.status_code,200)

    def test_list_of_users(self):
        count=5
        self.create_user(count)
        response= self.client.get(reverse('users'),format='json')
        self.assertEqual(len(response.data),count)

    def test_filter_accending_http(self):
        pass
    def test_filter_deccending_http(self):
        pass
    # filme add shode titlesh to movies baashe 
    # age hich filmi nabood api error monaseb bede 
    # logout tokena ro khaali kone 
    # age user rating nadasht error monaseb bede 
    # rating jadid karbar ezafe beshe 
    # user valid vared beshe 
    # usera ro dorost neshoon bede 
    pass