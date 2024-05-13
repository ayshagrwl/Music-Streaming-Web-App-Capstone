from flask import Blueprint, request
from flask_restful import Resource, reqparse, abort, fields, marshal_with
from functools import wraps #Used to make a decorator for RBAC 
from flask_jwt_extended import jwt_required, get_jwt_identity, get_current_user
from . import models
from .packages import db
from datetime import datetime
import os
from werkzeug.utils import secure_filename

views = Blueprint('views',__name__)

# This Decorator is used to implement RBAC (Role Based Access Control)
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not (get_current_user().role=='creator' or get_current_user().role=='admin'):
            abort(403, description = "You are not authorized to perform this action")
        return f(*args, **kwargs)
    return decorated_function

search_parser = reqparse.RequestParser()

home_fields = {
    "user_id": fields.Integer,
    "name": fields.String,
    "email": fields.String,
    "albums": fields.List(fields.Nested({
        "album_id": fields.Integer,
        "album_name": fields.String,
        "artist": fields.String,
        "genre": fields.String,
        "owner": fields.Integer,
        "songs": fields.List(fields.Nested({
            "song_id": fields.Integer,
            "song_name": fields.String,
            "rating": fields.Integer,
            "duration": fields.Integer,
            "album_id": fields.Integer,
            "is_flagged": fields.Boolean,
            "ratings": fields.List(fields.Nested({
                "rating_id": fields.Integer,
            }))
        }))
    })),
    "metrics": fields.List(fields.Nested({
        "total_playlist": fields.Integer,
        "total_creator_user": fields.Integer,
        "total_rating": fields.Integer,
        "total_songs": fields.Integer,
    })),
    }





class Home(Resource):

    @jwt_required()
    @marshal_with(home_fields)
    def get(self):
        current_user = get_current_user()
        if current_user.role=='admin': 
            total_creators = models.User.query.filter(models.User.role=='creator').count()
            
            total_playlist = models.Playlist.query.count()
            total_songs = models.Song.query.count()
            total_rating = models.Rating.query.count()
            
            
            albums = db.session.query(models.Album).all()
            current_user.albums = albums
            current_user.metrics = ({"total_playlist":total_playlist,"total_creator_user":total_creators,"total_rating":total_rating,"total_songs":total_songs})
            return current_user, 200
        elif current_user.role=='creator':
            user_id = get_current_user().user_id
            albums = db.session.query(models.Album).filter(models.Album.owner==user_id).all()
            # albums = db.session.query(models.Album).join(models.User).filter(models.User.user_id == models.Album.owner).all()
            current_user.albums = albums
            print(albums)
            return current_user, 200
        else:
            albums = db.session.query(models.Album).all()
            current_user.albums = albums
            print(current_user.role)
            return current_user, 200

class Album(Resource):

    album_fields = {
    "album_name": fields.String,
    "genre": fields.String,
    "artist": fields.String,
    }

    @jwt_required()
    @admin_required
    @marshal_with(album_fields)
    def get(self):
        album_id = request.args.get('album_id')
        album = models.Album.query.get(int(album_id))
        if not album:
            return {"message": "Album not found"}, 404
        else:
            return album, 200


    album_post_parser = reqparse.RequestParser()
    album_post_parser.add_argument("album_name", type=str, help="Album name is required", required=True)
    album_post_parser.add_argument("genre", type=str, help="Album Genre is required", required=True)
    album_post_parser.add_argument("artist", type=str, help="Artist is required", required=True)


    @jwt_required()
    @admin_required
    def post(self):

        req_args = self.album_post_parser.parse_args()
        album_name = req_args["album_name"]
        genre = req_args["genre"]
        artist = req_args["artist"]

        new_album = models.Album(album_name = album_name, genre=genre, artist=artist, owner = get_current_user().user_id)
        db.session.add(new_album)
        db.session.commit()
        return {"message": "Album added successfully"}, 200


    album_patch_parser = reqparse.RequestParser()
    album_patch_parser.add_argument("album_id", type=int, help="Album id is required", required=True)
    album_patch_parser.add_argument("album_name", type=str, help="Album name is required", required=True)
    album_patch_parser.add_argument("genre", type=str, help="Album Genre is required", required=True)
    album_patch_parser.add_argument("artist", type=str, help="Artist is required", required=True)

    @jwt_required()
    @admin_required
    def patch(self):
        
        req_args = self.album_patch_parser.parse_args()
            
        album_id = req_args["album_id"]
        album_name = req_args["album_name"]
        genre = req_args["genre"]
        artist = req_args["artist"]

        album = models.Album.query.filter_by(album_id = album_id).first()
        if not album:
            return {"message": "Album not found"}, 404
        else:
            album.album_name = album_name
            album.genre = genre
            album.artist = artist
            db.session.commit()

            return {"message": "Album updated successfully"}, 200
        
    
    @jwt_required()
    @admin_required
    def delete(self):
        
        album_id = request.args.get('album_id')
        album = models.Album.query.get(int(album_id))
        
        if album:
            db.session.delete(album)
            db.session.commit()

            return {"message": "Album deleted successfully"}, 200

        else:
            return {"message": "Album not found"}, 404



class Song(Resource):

    song_fileds = {
    "song_name": fields.String,
    "rating": fields.Integer,
    "lyrics": fields.String,
    "duration": fields.Integer,
    "date_created": fields.String,
    "song_path": fields.String,
    "album": fields.Nested({
            "album_id": fields.Integer,
            "album_name": fields.String,
            "genre": fields.String,
            "artist": fields.String})
    }

    

    @jwt_required()
    @marshal_with(song_fileds)
    def get(self):
        song_id = request.args.get('song_id')
        song = models.Song.query.get(int(song_id))
        if not song:
            return {"message": "Song not found"}, 404
        else:
            return song, 200


    @jwt_required()
    @admin_required
    def post(self):
        file = request.files['file']
        print(file)
        path = os.path.join(os.getcwd()+'/../Frontend/lyrics',file.filename)
        file.save(path)
        
        song_name = request.form.get('song_name')
        rating = request.form.get('rating')
        lyrics = request.form.get('lyrics')
        duration = request.form.get('duration')
        date_created = datetime.strptime(request.form.get('date_created'),'%Y-%m-%d').date()
        album_id = request.form.get('album_id')

        album = models.Album.query.filter_by(album_id=album_id).first()
        if not album:
            return {'message': 'No such Album exists'}, 404
        else:
            new_song = models.Song(song_name=song_name, rating=rating, lyrics=lyrics, duration=duration, date_created=date_created, song_path=file.filename, album_id=album_id)
            db.session.add(new_song)
            db.session.commit()
            return {"message" : "Song successfully added"},200
    



    song_patch_parser = reqparse.RequestParser()
    song_patch_parser.add_argument("song_name", type=str, help="Song name is required")
    song_patch_parser.add_argument("rating", type=int, help="Rating is required")
    song_patch_parser.add_argument("lyrics", type=str, help="Lyrics is required")
    song_patch_parser.add_argument("duration", type=int, help="Duration is required")
    song_patch_parser.add_argument("date_created", type=lambda x: datetime.strptime(x, '%Y-%m-%d').date())
    song_patch_parser.add_argument("flagged", type=bool, help="It is used to flag a song")

    @jwt_required()
    #@admin_required
    def patch(self):
        
        song_id = request.args.get('song_id')
        print(song_id)
        req_args = self.song_patch_parser.parse_args()

        song_name = req_args["song_name"]
        rating = req_args["rating"]
        lyrics = req_args["lyrics"]
        duration = req_args["duration"]
        date_created = req_args["date_created"]
        flagged = req_args["flagged"]

        print(flagged)
        song = models.Song.query.get(int(song_id))
        if flagged:
            song.is_flagged = flagged
            db.session.commit()
            return {"message": "Song is flagged successfully"}, 200

        if not song:
            return {"message": "Song not found"}, 404
        
        else:
            song.song_name = song_name
            song.rating = rating
            song.lyrics = lyrics
            song.duration = duration
            song.date_created = date_created

            db.session.commit()

            return {"message": "Song updated successfully"}, 200

    
    
    @jwt_required()
    @admin_required
    def delete(self):
        
        song_id = request.args.get('song_id')
        song = models.Song.query.get(int(song_id))

        if not song:
            return {"message": "Song not found"}, 404
        else:
            db.session.delete(song)
            db.session.commit()

            return {"message": "Song deleted successfully"}, 200
            

            
class Playlist(Resource):

    playlist_fields = {
            "id": fields.Integer,
            "playlist_name": fields.String,
        }

    
    @jwt_required()
    @marshal_with(playlist_fields)
    def get(self):
        
        user_id = get_jwt_identity()
        playlists = models.Playlist.query.filter_by(user=user_id).all()

        if not playlists:
            return {"message": "Playlists not found"}, 404
        else:
            return playlists, 200


    playlists_post_parser = reqparse.RequestParser()
    playlists_post_parser.add_argument("playlist_name", type=str, help="Playlist name is required", required=True)

    

    @jwt_required()
    def post(self):
        
        req_args = self.playlists_post_parser.parse_args()
        playlist_name = req_args["playlist_name"]
        user_id = get_jwt_identity()

        
        new_playlist = models.Playlist(playlist_name=playlist_name, user=user_id)
        db.session.add(new_playlist)
        db.session.commit()

        return {"message": "Playlist has been created successfully"}, 200
    
    @jwt_required()
    def delete(self):
        playlist_id = request.args.get('playlist_id')
        playlist = models.Playlist.query.get(int(playlist_id))

        if playlist:
            models.PlaylistSong.query.filter_by(playlist_id=playlist_id).delete()

            db.session.delete(playlist)
            db.session.commit()
            return {"message": "Successfully playlist deleted"}
        else:
            return {"message": "Playlist not deleted"}

class Rating(Resource):

    rating_parser = reqparse.RequestParser()
    rating_parser.add_argument('user_id', type=int, required=True, help='User ID is required')
    rating_parser.add_argument('song_id', type=int, required=True, help='Song ID is required')
    rating_parser.add_argument('rating', type=int, required=True, help='Rating is required')

    # @jwt_required()
    def post(self):
        
        req_args = self.rating_parser.parse_args()
        user_id = req_args['user_id']
        song_id = req_args['song_id']
        rating = req_args['rating']

        existing = models.Rating.query.filter_by(user_id=user_id, song_id=song_id).first()
        if existing:
            return {"message": "You already rated this song"}, 200

        rating_song = models.Rating(user_id=user_id, song_id=song_id, rating = rating)
        db.session.add(rating_song)
        db.session.commit()

        return {"message": "Congrats, you have rated this Song"}, 200

class PlaylistSong(Resource):


    playlist_song_fields = {
            "playlist_id": fields.Integer,
            "song_id": fields.Integer,
            "playlist": fields.Nested({
                "playlist_name": fields.String,
            }),
            "song": fields.Nested({
                "song_name": fields.String,
                "album":fields.Nested({
                    'album_name': fields.String
                })
            }),
        }

    @jwt_required()
    @marshal_with(playlist_song_fields)
    def get(self):
        playlist_id = request.args.get('playlist_id')
        # playlist_id = req_args['playlist_id']
        songs = models.PlaylistSong.query.filter_by(playlist_id=playlist_id).all()
        return songs, 200


    playlist_song_parser = reqparse.RequestParser()
    playlist_song_parser.add_argument('playlist_id', type=int, required=True, help='Playlist ID is required')
    playlist_song_parser.add_argument('song_id', type=int, required=True, help='Song ID is required')

    @jwt_required()
    @marshal_with(playlist_song_fields)
    def post(self):
        
        req_args = self.playlist_song_parser.parse_args()
        playlist_id = req_args['playlist_id']
        song_id = req_args['song_id']
        # song_id = request.args.get('song_id')

        existing = models.PlaylistSong.query.filter_by(playlist_id=playlist_id, song_id=song_id).first()
        if existing:
            return {"message": "This song is already present in the playlist"}, 400

        playlist_song = models.PlaylistSong(playlist_id=playlist_id, song_id=song_id)
        db.session.add(playlist_song)
        db.session.commit()

        return {"message": "Song has successfullly added to playlist"}, 200


# Use to get data for search results in home page
class Search(Resource):

        search_song_fields = {
        "songs": fields.List(fields.Nested({
            'song_id': fields.Integer,
            'song_name': fields.String,
            'rating': fields.Integer,
            'album_id': fields.Integer,
            'album_name': fields.String,
            'artists': fields.String,
            'genre': fields.String,
            }))
        }

        @jwt_required()
        @marshal_with(search_song_fields)
        def get(self):
            search_query = request.args.get('searchQuery')
            
            # songs = models.Song.query.filter((models.Song.rating.like("%"+search_query+"%")) | (models.Song.song_name.like("%"+search_query+"%")) | (models.Song.tags.like("%"+search_query+"%"))).all()
            songs = models.Song.query.join(models.Song.album).filter((models.Song.song_name.like("%"+search_query+"%")) | (models.Song.rating.like("%"+search_query+"%")) | (models.Album.album_name.like("%"+search_query+"%")) | (models.Album.artist.like("%"+search_query+"%")) | (models.Album.genre.like("%"+search_query+"%")))
            
            formatted_song_list = []
            for song in songs:
                formatted_song = {
                    'song_id': song.song_id,
                    'song_name': song.song_name,
                    'rating': song.rating,
                    'album_name': song.album.album_name,
                    'artist': song.album.artist,
                    'genre': song.album.genre,
                    'album_id': song.album_id,
                    
                }
                formatted_song_list.append(formatted_song)

            return { "songs" : formatted_song_list}, 200
            



