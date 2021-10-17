import json
from json import requests
from song import Song
from playlist import Playlist


class SpotifyClient:

    def __init__(self, authtok, user) -> None:
        self.authtok = authtok
        self.user = user

    def get_request(self, url):
        response = requests.get(
            url,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.authtok}"
            }
        )
        return response

    def post_request(self, url, data):
        respnse = requests.post(
            url,
            data=data,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.authtok}"
            }
        )

    def recent_tracks(self, num=15):
        url = f"https://api.spotify.com/v1/me/player/recently-played?limit={num}"
        response = self.get_request(url)
        json = response.json()
        songs = [Song(song["track"]["name"], song["track"]["id"],
                      song["track"]["artists"][0]["name"]) for song in json["items"]]
        return songs

    def get_recs(self, seeds, limit=50):
        seed_url = ""
        for seed in seeds:
            seed_url += seed.id + ","
        seed_url = seed_url[:-1]
        url = f"https://api.spotify.com/v1/recommendations?seed_tracks{seed_url}&limit={limit}"
        response = self.get_request(url)
        json = response.json()
        songs = [Song(song["name"], song["id"], song['artists'][0]["name"])
                 for song in json["tracks"]]
        return songs

    def playlist_create(self, name):
        data = json.dumps({
            "name": name,
            "description": "Reccommended tracks",
            "public": True
        }
        )
        url = f"https://api.spotify.com/v1/users/{self.user}/playlists"
        response = self.post_request(url, data)
        playlistid = response["id"]
        playlist = Playlist(name, playlistid)
        return playlist

    def fill_playlist(self, playlist, songs):
        uris = [song.spotify_uri() for song in songs]
        data = json.dumps(uris)
        url = f"https://api.spotify.com/v1/playlists/{playlist.id}/tracks"
        response = self.post_request(url, data)
        rjson = response.json()
        return rjson
