from django.urls import path
from .  import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'movies',views.MovieViewsets,basename='movies')
urlpatterns = [
    path("logout/" , views.logout)
]

urlpatterns+=router.urls
