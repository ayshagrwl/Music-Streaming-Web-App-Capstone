from flask import Blueprint
from flask_restful import Api
from .auth import SignUp, Login, Logout, Admin_login, ToggleCreator
from .views import Home, Album, Song, Search, Rating, Playlist, PlaylistSong


api_bp = Blueprint('api', __name__)
api = Api(api_bp)

# Authorisation API
api.add_resource(SignUp, '/signup')
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')
api.add_resource(Admin_login, "/admin")

# Home API
api.add_resource(Home, '/home')

# Album API
api.add_resource(Album, '/album')

# Song API
api.add_resource(Song, '/song')

# Rating API
api.add_resource(Rating, '/rating')

# Playlist API
api.add_resource(Playlist, '/playlists')

# Playlist_Song API
api.add_resource(PlaylistSong, '/playlistsong')

# Search API
api.add_resource(Search, '/search')

# Toggle for Creator API
api.add_resource(ToggleCreator, '/toggle-creator')
