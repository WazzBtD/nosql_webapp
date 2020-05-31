from django.urls import path

from . import views


app_name = 'main'


urlpatterns = [
    path('', views.homepage_request, name='homepage'),
    path("search/", views.search_request, name="search"),
    path("signup/", views.signup_request, name="signup"),
    path("login/", views.login_request, name="login"),
    path("logout/", views.logout_request, name="logout"),
    path('artists/', views.ArtistListView.as_view(), name='artist-list'),
    path('genres/', views.GenreListView.as_view(), name='genre-list'),
    path('albums/', views.AlbumListView.as_view(), name='album-list'),
    path('labels/', views.LabelListView.as_view(), name='label-list'),
    path('songs/', views.SongListView.as_view(), name='song-list'),
    path('artist/<int:pk>', views.ArtistDetailView.as_view(), name='artist-detail'),
    path('genre/<int:pk>', views.GenreDetailView.as_view(), name='genre-detail'),
    path('album/<int:pk>', views.AlbumDetailView.as_view(), name='album-detail'),
    path('label/<int:pk>', views.LabelDetailView.as_view(), name='label-detail'),
    path('song/<int:pk>/', views.SongDetailView.as_view(), name='song-detail'),

]




