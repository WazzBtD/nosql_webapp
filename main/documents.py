from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl.registries import registry
from .models import Album, Artist, Song, Label, Genre


@registry.register_document
class SongDocument(Document):
    class Index:
        # Name of the Elasticsearch index
        name = 'songs'
        # See Elasticsearch Indices API reference for available settings
        settings = {'number_of_shards': 1,
                    'number_of_replicas': 0}

    class Django:
        model = Song  # The model associated with this Document
        # The fields of the model you want to be indexed in Elasticsearch
        fields = [
            'title',
            'lyrics',
            'language',
        ]


@registry.register_document
class ArtistDocument(Document):
    class Index:
        # Name of the Elasticsearch index
        name = 'artists'
        # See Elasticsearch Indices API reference for available settings
        settings = {'number_of_shards': 1,
                    'number_of_replicas': 0}

    class Django:
        model = Artist # The model associated with this Document
        # The fields of the model you want to be indexed in Elasticsearch
        fields = [
            'name',
            'bio',
        ]


@registry.register_document
class AlbumDocument(Document):
    class Index:
        # Name of the Elasticsearch index
        name = 'albums'
        # See Elasticsearch Indices API reference for available settings
        settings = {'number_of_shards': 1,
                    'number_of_replicas': 0}

    class Django:
        model = Album # The model associated with this Document
        # The fields of the model you want to be indexed in Elasticsearch
        fields = [
            'title',
            'description',
            'published',
        ]


@registry.register_document
class LabelDocument(Document):
    class Index:
        # Name of the Elasticsearch index
        name = 'labels'
        # See Elasticsearch Indices API reference for available settings
        settings = {'number_of_shards': 1,
                    'number_of_replicas': 0}

    class Django:
        model = Label # The model associated with this Document
        # The fields of the model you want to be indexed in Elasticsearch
        fields = [
            'name',
        ]


@registry.register_document
class GenreDocument(Document):
    class Index:
        # Name of the Elasticsearch index
        name = 'genres'
        # See Elasticsearch Indices API reference for available settings
        settings = {'number_of_shards': 1,
                    'number_of_replicas': 0}

    class Django:
        model = Genre # The model associated with this Document
        # The fields of the model you want to be indexed in Elasticsearch
        fields = [
            'name',
            'description',
        ]