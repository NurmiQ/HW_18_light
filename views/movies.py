from flask import request
from flask_restx import Resource, Namespace
from setup_db import db
from models import Movie, MovieSchema

movie_ns = Namespace('movies')
movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)


@movie_ns.route('/')
class MoviesView(Resource):
    def get(self):
        director = request.args.get("director_id")
        genre = request.args.get("genre_id")
        year = request.args.get("year")
        movie = db.session.query(Movie)
        if director is not None:
            movie = movie.filter(Movie.director_id == director)
        if genre:
            movie = movie.filter(Movie.genre_id == genre)
        if year is not None:
            movie = movie.filter(Movie.year == year)
        movies = movie.all()
        return movies_schema.dump(movies), 200

    def post(self):
        data = request.json
        new_movie = Movie(**data)
        with db.session.begin():
            db.session.add(new_movie)
        return "", 201


@movie_ns.route('/<int:bid>')
class MovieView(Resource):
    def get(self, bid):
        movie = db.session.query(Movie).get(bid)
        return movie_schema.dump(movie), 200

    def put(self, bid):
        movie = db.session.query(Movie).get(bid)
        req_json = request.json
        movie.director = req_json.get("director")
        movie.description = req_json.get("description")
        movie.trailer = req_json.get("trailer")
        movie.year = req_json.get("year")
        movie.rating = req_json.get("rating")
        movie.genre_id = req_json.get("genre_id")
        movie.director_id = req_json.get("director_id")
        db.session.add(movie)
        db.session.commit()
        return "", 204

    def delete(self, bid):
        movie = db.session.query(Movie).get(bid)
        db.session.delete(movie)
        db.session.commit()
        return "", 204
