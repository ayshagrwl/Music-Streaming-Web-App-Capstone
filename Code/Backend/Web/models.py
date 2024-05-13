from .packages import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from datetime import datetime


class User(db.Model, UserMixin):
    user_id = db.Column(db.Integer,primary_key = True)
    email = db.Column(db.String(150),unique = True, nullable = False)
    password = db.Column(db.String(150), nullable = False)
    name = db.Column(db.String(150), nullable = False)
    albums = db.relationship('Album')
    last_login = db.Column(db.DateTime, default=datetime.utcnow())
    
    role = db.Column(db.String(50), nullable = False, default='user')
    playlists = db.relationship('Playlist')
    ratings = db.relationship('Rating', back_populates='user')

    
class Album (db.Model):
    album_id = db.Column(db.Integer, primary_key = True)
    album_name = db.Column(db.String(250), nullable = False)

    genre = db.Column(db.String(250))
    artist = db.Column(db.String(250))
    owner = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable = False)
    songs = db.relationship('Song',back_populates='album' ,cascade='all, delete-orphan')



    

class Song(db.Model):
    song_id = db.Column(db.Integer, primary_key = True)
    song_name = db.Column(db.String(250))
    rating = db.Column(db.Integer)
    lyrics = db.Column(db.Text)
    duration = db.Column(db.Integer)
    date_created = db.Column(db.Date, default=func.now())

    album_id = db.Column(db.Integer, db.ForeignKey('album.album_id', ondelete = 'CASCADE'), nullable = False)
    album = db.relationship('Album', back_populates='songs')
   
    song_path = db.Column(db.String(500))
    is_flagged = db.Column(db.Boolean, default=False)
    
    ratings = db.relationship('Rating', back_populates='song')
    playlists = db.relationship('PlaylistSong', back_populates='song')

class Rating(db.Model):
    rating_id = db.Column(db.Integer, primary_key=True)
    song_id = db.Column(db.Integer, db.ForeignKey('song.song_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    rating = db.Column(db.Integer)

    user = db.relationship('User', back_populates='ratings')
    song = db.relationship('Song', back_populates='ratings')
    
class Playlist(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    playlist_name = db.Column(db.String(500))
    user = db.Column(db.Integer, db.ForeignKey('user.user_id'))

    playlist_songs = db.relationship('PlaylistSong', back_populates='playlist')

class PlaylistSong(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    playlist_id = db.Column(db.Integer, db.ForeignKey('playlist.id'))
    song_id = db.Column(db.Integer, db.ForeignKey('song.song_id'))

    playlist = db.relationship('Playlist', back_populates='playlist_songs')
    song = db.relationship('Song', back_populates='playlists')


  