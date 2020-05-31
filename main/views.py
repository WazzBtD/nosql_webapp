from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout, authenticate, login
from django.shortcuts import redirect, render
from .forms import SignUpForm
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from django_elasticsearch_dsl.search import Search

from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from django.utils.decorators import method_decorator

from .models import SongByArtist, Song, Artist, Label, Genre, Album
from .cassandra import session, select_by_album_stmt, select_by_artist_stmt, select_by_genre_stmt, select_by_label_stmt


@method_decorator(vary_on_cookie, name='dispatch')
@method_decorator(cache_page(60 * 1), name='dispatch')
class ArtistListView(ListView):

    model = Artist

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


@method_decorator(vary_on_cookie, name='dispatch')
@method_decorator(cache_page(60 * 1), name='dispatch')
class SongListView(ListView):

    model = Song

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


@method_decorator(vary_on_cookie, name='dispatch')
@method_decorator(cache_page(60 * 1), name='dispatch')
class GenreListView(ListView):

    model = Genre

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


@method_decorator(vary_on_cookie, name='dispatch')
@method_decorator(cache_page(60 * 1), name='dispatch')
class LabelListView(ListView):

    model = Label

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


@method_decorator(vary_on_cookie, name='dispatch')
@method_decorator(cache_page(60 * 1), name='dispatch')
class AlbumListView(ListView):

    model = Album

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


@method_decorator(vary_on_cookie, name='dispatch')
@method_decorator(cache_page(60 * 1), name='dispatch')
class SongDetailView(DetailView):

    model = Song

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


@method_decorator(vary_on_cookie, name='dispatch')
@method_decorator(cache_page(60 * 1), name='dispatch')
class ArtistDetailView(DetailView):

    model = Artist

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['songs'] = session.execute(select_by_artist_stmt, [self.kwargs['pk']])
        return context


@method_decorator(vary_on_cookie, name='dispatch')
@method_decorator(cache_page(60 * 1), name='dispatch')
class AlbumDetailView(DetailView):

    model = Album

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['songs'] = session.execute(select_by_album_stmt, [self.kwargs['pk']])
        return context


@method_decorator(vary_on_cookie, name='dispatch')
@method_decorator(cache_page(60 * 1), name='dispatch')
class GenreDetailView(DetailView):

    model = Genre

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['songs'] = session.execute(select_by_genre_stmt, [self.kwargs['pk']])
        return context


@method_decorator(vary_on_cookie, name='dispatch')
@method_decorator(cache_page(60 * 1), name='dispatch')
class LabelDetailView(DetailView):

    model = Label

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['songs'] = session.execute(select_by_label_stmt, [self.kwargs['pk']])
        return context


def view_404(request, exception=None):
    return redirect('/')


@login_required(login_url='/login')
def homepage_request(request):
    return render(request=request,
                  template_name="main/homepage.html")


def signup_request(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(
                request, f"New account created. Welcome {username}!")
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect("main:homepage")

        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg}: {form.error_messages[msg]}")

            return render(request=request,
                          template_name="main/signup.html",
                          context={"form": form})

    return render(request=request,
                  template_name="main/signup.html",
                  context={"form": SignUpForm()})


@login_required(login_url='/login')
def logout_request(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("/")


def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}")
                return redirect('main:homepage')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    return render(request=request,
                  template_name="main/login.html",
                  context={"form": AuthenticationForm()})


@login_required(login_url='/login')
def search_request(request):
    if request.method == 'GET':
        if q := request.GET.get('q', None):
            object_list = []
            search = Search(index=['songs', 'artists', 'albums', 'labels', 'genres'])
            objects = search.from_dict({
                "query": {
                    "dis_max": {
                        "queries": [
                            {"multi_match": {
                                "query": q,
                                "type": "phrase",
                                "fields": [
                                    "title^20",
                                    "lyrics^10",
                                    "name^100",
                                    "description^50"
                                ]
                            }},
                            {"multi_match": {
                                "query": q,
                                "fuzziness": "AUTO",
                                "fields": [
                                    "title^2",
                                    "lyrics",
                                    "name^10",
                                    "description^5"
                                ]
                            }}
                        ]
                    }
                }
            })

            for obj in objects:
                print(obj)

                row = {
                    'id': obj.meta.id,
                    'score': obj.meta.score,
                    'url': 'main:' + obj.meta.index[:-1] + '-detail',
                    'model': obj.meta.index,
                }
                if obj.meta.index == 'songs':
                    row['text'] = f'Song: {obj.title}'
                elif obj.meta.index == 'artists':
                    row['text'] = f'Artist: {obj.name}'
                elif obj.meta.index == 'labels':
                    row['text'] = f'Label: {obj.name}'
                elif obj.meta.index == 'genres':
                    row['text'] = f'Genre: {obj.name}'
                elif obj.meta.index == 'albums':
                    row['text'] = f'Album: {obj.title}'
                object_list.append(row)
            return render(request=request,
                          template_name="main/search.html",
                          context={'object_list': object_list})

    return render(request=request,
                  template_name="main/search.html",
                  context={'object_list': None})