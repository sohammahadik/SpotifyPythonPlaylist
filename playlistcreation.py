import os
from spotifycli import SpotifyClient


def main():

    SPOTIFY_AUTHORIZATION_TOKEN = input(
        "Follow this link (https://developer.spotify.com/console/get-current-user/) and log into Spotify. Copy and paste the OAuth Token here.")
    SPOTIFY_USER_ID = input(
        "Follow this link (https://developer.spotify.com/console/post-playlists/) and log into Spotify. Select 'playlist-modify-public', 'playlist-modify-private', and 'user-read-recently-played'. Copy and paste the OAuth Token here.")

    spot_cli = SpotifyClient(
        os.getenv(SPOTIFY_AUTHORIZATION_TOKEN), os.getenv(SPOTIFY_USER_ID))

    num_tracks = int(input("How many recent songs do you want to use?"))
    recent_tracks = spot_cli.recent_tracks(num_tracks)

    for index, song in enumerate(recent_tracks):
        print(f"{index+1}- {song}")

    seed_ind = input(
        "Enter the indices of five tracks to use as seeds (seperate by spaces): ")
    seed_ind = seed_ind.split()
    seeds = [recent_tracks[int(ind)-1] for ind in seed_ind]

    recs = spot_cli.get_recs(seeds)
    for index, song in enumerate(recs):
        print(f"{index+1}- {song}")

    name = input("What do you want to name the playlist? ")
    playlist = spot_cli.playlist_create(name)
    spot_cli.fill_playlist(playlist, recs)
    print(f"Reccommendations have been uploaded to your new playlist {name}!")


if __name__ == '__main__':
    main()
