from flask_restx import Resource, Namespace
from setup_db import db
from models import Genre, GenreSchema

genre_ns = Namespace('genres')
genre_schema = GenreSchema()
genres_schema = GenreSchema(many=True)


@genre_ns.route('/')
class GenresView(Resource):
    def get(self):
        genres = db.session.query(Genre).all()
        return genres_schema.dump(genres), 200

@genre_ns.route('/<int:bid>')
class GenreView(Resource):
    def get(self, bid):
        genre = db.session.query(Genre).get(bid)
        return genre_schema.dump(genre), 200





