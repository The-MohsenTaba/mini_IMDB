from django.urls import path
from .  import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'movies',views.MovieViewsets,basename='movies')
urlpatterns = [
    path("logout/" , views.logout , name="logout"),
    path("my-ratings/",views.MyRatings.as_view(),name="my-ratings"),
    path("authenticated/",views.is_logged_in,name="auth"),
    path("sign-up/",views.register_user, name="sign-up"),
    path("users/",views.all_users, name='users'),
    path("mongo/persons/", views.mongo_person_view, name="mongo-persons"),
    path("mongo/movies/", views.MongoMovieClass.as_view(), name="mongomovies"),
    path("mongo/rating/", views.mongo_rating_view,name="mongoratings"),

]

urlpatterns+=router.urls
