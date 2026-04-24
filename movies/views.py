from django.shortcuts import render, get_object_or_404, redirect
from .models import Movie

from .forms import MovieForm

def movie_list(request):
    movies = Movie.objects.all().order_by('-created_at')

    query = request.GET.get('q', '').strip()
    genre = request.GET.get('genre', '').strip()

    # 🔍 Search
    if query:
        movies = movies.filter(title__icontains=query)

        # 🎯 Genre filter (FIXED)
    if genre:
        movies = movies.filter(genre__iexact=genre)

        # --- Cookies: Recently Viewed ---
    recent_ids = request.COOKIES.get('recently_viewed', '')
    recent_ids = [int(i) for i in recent_ids.split(',') if i]
    recent_movies = Movie.objects.filter(pk__in=recent_ids)

    context = {
        'movies': movies,
        'query': query,
        'genre': genre,
        'genre_choices': Movie.GENRE_CHOICES if hasattr(Movie, 'GENRE_CHOICES') else [],
        'recent_movies': recent_movies,
    }
   
    return render(request, 'movies/movie_list.html', context)

def movie_detail(request, pk):
    movie = get_object_or_404(Movie, pk=pk)

    response = render(request, 'movies/movie_detail.html', {'movie': movie})

    # Read existing cookie
    recent_ids = request.COOKIES.get('recently_viewed', '')
    id_list = [i for i in recent_ids.split(',') if i]

    # Prepend current movie, deduplicate, keep last 5
    movie_id = str(pk)
    if movie_id in id_list:
        id_list.remove(movie_id)
    id_list.insert(0, movie_id)
    id_list = id_list[:5]

        # Set cookie (expires in 7 days)
    response.set_cookie('recently_viewed', ','.join(id_list), max_age=7*24*3600)

    return response
    
def movie_create(request):
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES)  # FILES for image
        if form.is_valid():
            form.save()
            return redirect('movies:movie_list')  # PRG: redirect after POST
    else:
        form = MovieForm()

    return render(request, 'movies/movie_form.html', {'form': form, 'action': 'Create'})  

# def movie_update(request, pk):
#     movie = get_object_or_404(Movie, pk=pk)
#     if request.method == 'POST':
#         form = MovieForm(request.POST, request.FILES, instance=movie)
#         if form.is_valid():
#             form.save()
#             return redirect('movies:movie_detail', pk=movie.pk)
#     else:
#         form = MovieForm(instance=movie)  # Pre-populates with existing data

#     return render(request, 'movies/movie_form.html', {'form': form, 'action': 'Update'})

def movie_update(request, pk):
    movie = get_object_or_404(Movie, pk=pk)

    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES, instance=movie)

        if form.is_valid():
            movie = form.save(commit=False)

            # 🔥 IMPORTANT FIX
            if request.FILES.get('image'):
                movie.image = request.FILES['image']

            movie.save()
            return redirect('movies:movie_detail', pk=movie.pk)

        else:
            form = MovieForm(instance=movie)

        return render(request, 'movies/movie_form.html', {'form': form, 'action': 'Update'})
def movie_delete(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    if request.method == 'POST':
        movie.delete()
        return redirect('movies:movie_list')
    return render(request, 'movies/movie_confirm_delete.html', {'movie': movie})          