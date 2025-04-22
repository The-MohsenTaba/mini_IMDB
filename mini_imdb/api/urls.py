from django.urls import path
from .  import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'movies',views.MovieViewsets,basename='movies')
urlpatterns = [
    #path("movies" , views.MoviesView.as_view())
]

urlpatterns+=router.urls
