from django.contrib import admin
from api.models import*
from django.contrib.auth.admin import UserAdmin
# Register your models here.
class MovieAdmin(admin.ModelAdmin):
    list_display=['title','rating_count','average_rating','genere']
admin.site.register(User,UserAdmin)
admin.site.register(Movie,MovieAdmin)
admin.site.register(Vote)
admin.site.register(Person)