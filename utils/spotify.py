import spotipy
from spotipy import oauth2
from dotenv import load_dotenv
from os import getenv

load_dotenv()

client_id = getenv("spotify_client_id")
client_secret = getenv("spotify_client_secret")
redirect_uri = getenv("redirect_uri")

oauth = oauth2.SpotifyOAuth(client_id, client_secret, redirect_uri, scope="user-read-currently-playing user-read-recently-played")

def get_token(code: str):
    return oauth.get_access_token(code)['access_token']