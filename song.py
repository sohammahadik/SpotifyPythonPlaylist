class Song:

    def __init__(self, name, trackid, artist) -> None:
        self.name = name
        self.trackid = trackid
        self.artist = artist

    def spotify_uri(self) -> str:
        return f"spotify:track:{self.trackid}"

    def __str__(self) -> str:
        return f"{self.name} by {self.artist}"
