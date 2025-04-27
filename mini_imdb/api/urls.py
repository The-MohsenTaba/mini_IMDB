from django.urls import path
from .  import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'movies',views.MovieViewsets,basename='movies')
urlpatterns = [
    path("logout/" , views.logout),
    path("my-ratings/",views.MyRatings.as_view()),
    path("authenticated/",views.is_logged_in),
    path("sign-up/",views.register_user),
    path("users/",views.all_users)
]

urlpatterns+=router.urls
