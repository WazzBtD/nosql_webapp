from django.contrib import admin

from .models import Song, Artist, Album, Genre, Label


admin.site.register(Song)
admin.site.register(Artist)
admin.site.register(Album)
admin.site.register(Genre)
admin.site.register(Label)

