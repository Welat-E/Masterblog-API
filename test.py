@app.route('/users/<int:user_id>/add_movie', methods=['GET', 'POST'])
def add_movie(user_id):
    API_KEY = '49526238'
    API_URL = "http://www.omdbapi.com/"

    if request.method == 'POST':
        title = request.form['name']
        params = {
            'apikey': API_KEY,
            't': title
        }
        response = requests.get(API_URL, params=params)

        if response.status_code == 200:
            movie_data = response.json()
            if movie_data.get('Response') == 'True':
                # Extrahiere alle benötigten Informationen
                name = movie_data.get('Title')
                director = movie_data.get('Director')
                year = movie_data.get('Year')
                rating = movie_data.get('imdbRating')  # API delivers it as string, maybe in float

                #creatin a new movie insert
                movie = Movie(
                    name=name,
                    director=director,
                    year=int(year) if year.isdigit() else None,  # convert in Integer, if possible
                    rating=float(rating) if rating else None,  # convert in Float, if there
                    user_id=user_id
                )
                db.session.add(movie)
                db.session.commit()
                return redirect(url_for('get_user_movies', user_id=user_id))
            else:
                #no movie found
                error_message = "Movie not found. Please try again."
                return render_template('add_movie.html', user_id=user_id, error=error_message)
        else:
            # API-request failed
            error_message = "Error with the request. Please try again later."
            return render_template('add_movie.html', user_id=user_id, error=error_message)

    return render_template('add_movie.html', user_id=user_id)