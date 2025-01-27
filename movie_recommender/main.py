from flask import Flask, render_template, request, redirect, url_for
from movies import movies_list, sort_movies_by_title, sort_movies_by_year, sort_movies_by_rating

app = Flask(__name__)

@app.route('/')
def index():
    # Сортировать фильмы по рейтингу для отображения популярных
    sorted_movies = sort_movies_by_rating(movies_list)
    popular_movies = sorted_movies[:5]
    return render_template('index.html', movies=popular_movies)

@app.route('/search', methods=['GET', 'POST'])
def search():
    title = request.form.get('title')
    genre = request.form.get('genre')
    year = request.form.get('year')
    rating = request.form.get('rating')
    description = request.form.get('description')
    language = request.form.get('language')
    sort_by = request.form.get('sort_by')

    filtered_movies = movies_list

    # Фильтрация по названию
    if title:
        filtered_movies = [movie for movie in filtered_movies if title.lower() in movie['title'].lower()]

    # Фильтрация по жанру
    if genre:
        filtered_movies = [movie for movie in filtered_movies if genre.lower() in movie['genre'].lower()]

    # Фильтрация по году
    if year:
        filtered_movies = [movie for movie in filtered_movies if movie['year'] == int(year)]

    # Фильтрация по рейтингу
    if rating:
        filtered_movies = [movie for movie in filtered_movies if movie.get('rating', 0) >= float(rating)]

    # Фильтрация по описанию
    if description:
        filtered_movies = [movie for movie in filtered_movies if description.lower() in movie['description'].lower()]

    # Фильтрация по языку
    if language:
        filtered_movies = [movie for movie in filtered_movies if language.lower() in movie['language'].lower()]

    # Сортировка
    if sort_by == 'title':
        filtered_movies = sort_movies_by_title(filtered_movies)
    elif sort_by == 'year':
        filtered_movies = sort_movies_by_year(filtered_movies)
    elif sort_by == 'rating':
        filtered_movies = sort_movies_by_rating(filtered_movies)

    return render_template('search.html', movies=filtered_movies, title=title, genre=genre, year=year, rating=rating, description=description, language=language, sort_by=sort_by)

@app.route('/random')
def random_movie():
    import random
    random_movie = random.choice(movies_list)
    return render_template('random.html', movie=random_movie)

@app.route('/add_movie', methods=['GET', 'POST'])
def add_movie():
    if request.method == 'POST':
        title = request.form.get('title')
        genre = request.form.get('genre')
        year = int(request.form.get('year'))
        description = request.form.get('description')
        language = request.form.get('language')

        new_movie = {
            'id': len(movies_list) + 1,
            'title': title,
            'genre': genre,
            'year': year,
            'rating': 0, 
            'language': language,
            'description': description,
            'user_ratings': [],
            'comments': []
        }

        movies_list.append(new_movie)
        return redirect(url_for('index'))

    return render_template('add_movie.html')

@app.route('/movie/<int:movie_id>', methods=['GET', 'POST'])
def movie_details(movie_id):
    movie = next((movie for movie in movies_list if movie['id'] == movie_id), None)

    if request.method == 'POST':
        # Добавление комментария
        comment = request.form.get('comment')
        if comment:
            movie['comments'].append(comment)

        # Добавление рейтинга
        rating = request.form.get('rating')
        if rating and 0 <= float(rating) <= 10:
            movie['user_ratings'].append(float(rating))
            movie['rating'] = sum(movie['user_ratings']) / len(movie['user_ratings'])

    return render_template('movie_details.html', movie=movie)

if __name__ == '__main__':
    app.run(debug=True)
