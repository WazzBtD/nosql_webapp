from djongo import models
from django.utils.datetime_safe import datetime
from django.contrib.auth.models import User
from cassandra.cqlengine import columns
from django_cassandra_engine.models import DjangoCassandraModel
from .cassandra import session, delete_by_artist_stmt, delete_by_album_stmt, delete_by_genre_stmt, delete_by_label_stmt


class Artist(models.Model):
    name = models.CharField(max_length=200)
    bio = models.TextField()
    rating = models.FloatField()

    def __str__(self):
        return self.name


class Album(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    published = models.DateField(default=datetime.now)
    rating = models.FloatField()

    def __str__(self):
        return self.title


class Genre(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.name


class Label(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Song(models.Model):
    title = models.CharField(max_length=200)
    language = models.CharField(max_length=200)
    length = models.IntegerField()
    lyrics = models.TextField()
    rating = models.FloatField()
    published = models.DateField(default=datetime.now)
    id_artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    id_album = models.ForeignKey(Album, on_delete=models.CASCADE)
    id_genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    id_label = models.ForeignKey(Label, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title} by {self.id_artist.name}'

    def save(self, *args, **kwargs):

        if self.id:  # record already existed. it's edit. we need to delete previous data
            old_self = Song.objects.get(pk=self.id)
            if old_self.id_artist != self.id_artist:
                session.execute(delete_by_artist_stmt, [self.id, old_self.id_artist.id])
            if old_self.id_album != self.id_album:
                session.execute(delete_by_album_stmt, [self.id, old_self.id_album.id])
            if old_self.id_genre != self.id_genre:
                session.execute(delete_by_genre_stmt, [self.id, old_self.id_genre.id])
            if old_self.id_genre != self.id_genre:
                session.execute(delete_by_label_stmt, [self.id, old_self.id_label.id])

        super().save(*args, **kwargs)
        session.execute("INSERT INTO song_by_artist (id_song, title, album, id_artist) VALUES (%s, %s, %s, %s)",
                        (self.id, self.title, self.id_album.title, self.id_artist.id))
        session.execute("INSERT INTO song_by_genre (id_song, title, artist, id_genre) VALUES (%s, %s, %s, %s)",
                        (self.id, self.title, self.id_artist.name, self.id_genre.id))
        session.execute("INSERT INTO song_by_label (id_song, title, artist, id_label) VALUES (%s, %s, %s, %s)",
                        (self.id, self.title, self.id_artist.name, self.id_label.id))
        session.execute("INSERT INTO song_by_album (id_song, title, artist, id_album) VALUES (%s, %s, %s, %s)",
                        (self.id, self.title, self.id_artist.name, self.id_album.id))

    def delete(self, *args, **kwargs):
        session.execute(delete_by_artist_stmt, [self.id, self.id_artist.id])
        session.execute(delete_by_album_stmt, [self.id, self.id_album.id])
        session.execute(delete_by_genre_stmt, [self.id, self.id_genre.id])
        session.execute(delete_by_label_stmt, [self.id, self.id_label.id])
        super().delete(*args, **kwargs)


# cass

class SongByArtist(DjangoCassandraModel):
    title = columns.Text()
    album = columns.Text()
    id_artist = columns.Integer(partition_key=True)
    id_song = columns.Integer(primary_key=True)

    class Meta:
        get_pk_field = 'id_song'


class SongByGenre(DjangoCassandraModel):
    title = columns.Text()
    artist = columns.Text()
    id_genre = columns.Integer(primary_key=True)
    id_song = columns.Integer(primary_key=True)

    class Meta:
        get_pk_field = 'id_song'


class SongByLabel(DjangoCassandraModel):
    title = columns.Text()
    artist = columns.Text()
    id_label = columns.Integer(primary_key=True)
    id_song = columns.Integer(primary_key=True)

    class Meta:
        get_pk_field = 'id_song'


class SongByAlbum(DjangoCassandraModel):

    title = columns.Text()
    artist = columns.Text()
    id_album = columns.Integer(primary_key=True)
    id_song = columns.Integer(primary_key=True)

    class Meta:
        get_pk_field = 'id_song'



