#!/usr/bin/env python3

# No __pychache__ I beg you
import sys
sys.dont_write_bytecode = True

from argparse import ArgumentParser
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import requests
import os
from dotenv import load_dotenv
from display import *


__author__ = "ENA"


def parser():
    parser = ArgumentParser()

    parser.add_argument(
        "-url",
        "--spotify-playlist-url",
        required=True,
        type=str,
        dest="url",
        help="Spotify playlist url",
    )
    parser.add_argument(
        "-name",
        "--AM-playlist-name",
        required=True,
        type=str,
        dest="name",
        help="Apple Music name for the transfered playlist",
    )
    parser.add_argument(
        "-o",
        "--output",
        required=False,
        default=False,
        type=bool,
        dest="output",
        help="'True' if you want the songs not found to be written in a txt file, 'False' if not",
    )

    return parser.parse_args()


def get_spotify_playlist_tracklist(sp, playlist_url):
    tracks = []
    results = sp.playlist_tracks(playlist_url)
    tracks.extend(results["items"])

    while results["next"]:
        results = sp.next(results)
        tracks.extend(results["items"])

    track_data = []
    for item in tracks:
        track = item["track"]
        track_data.append(
            {
                "name": track["name"],
                "artist": track["artists"][0]["name"],
                "album": track["album"]["name"],
            }
        )

    return track_data


def create_apple_music_playlist(am_playlist_name, track_ids):
    url = f"https://api.music.apple.com/v1/me/library/playlists"
    headers = {
        "Authorization": f"Bearer {APPLE_MUSIC_DEVELOPER_TOKEN}",
        "Music-User-Token": APPLE_MUSIC_USER_TOKEN,
    }
    data = {
        "attributes": {"name": am_playlist_name},
        "relationships": {
            "tracks": {
                "data": [{"id": track_id, "type": "songs"} for track_id in track_ids]
            }
        },
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 201:
        print(
            colored_text(f" ╰─ Playlist '{am_playlist_name}' created successfully!"),
            LGREEN,
        )
    else:
        print(
            colored_text(
                f" ╰─ Failed to create playlist: {response.status_code}, {response.text}",
                LRED,
            )
        )


def search_apple_music_track(track_name, artist_name):
    url = f"https://api.music.apple.com/v1/catalog/us/search"
    headers = {
        "Authorization": f"Bearer {APPLE_MUSIC_DEVELOPER_TOKEN}",
        "Music-User-Token": APPLE_MUSIC_USER_TOKEN,
    }
    params = {"term": f"{track_name} {artist_name}", "limit": 1, "types": "songs"}
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        if "results" in data and "songs" in data["results"]:
            return data["results"]["songs"]["data"][0]["id"]
    return None


def transfer_playlist(sp, spotify_playlist_id, am_playlist_name, output):
    print(colored_text(f"[+] Indexing songs from Spotify playlist...", DGREY))

    spotify_tracks = get_spotify_playlist_tracklist(sp, spotify_playlist_id)

    # Print number of songs found in the playlist
    if len(spotify_tracks) > 0:
        print(
            colored_text(
                f" ╰─ Found {len(spotify_tracks)} tracks in the playlist", GREEN
            )
        )
    else:
        exit(colored_text(" ╰─ No song was found in the playlist", LRED))

    apple_music_track_ids = []

    print(
        colored_text(f"[+] Searching for the indexed tracks in Apple Music...", DGREY)
    )
    not_found = []
    for track in spotify_tracks:
        track_id = search_apple_music_track(track["name"], track["artist"])
        if track_id:
            apple_music_track_ids.append(track_id)
        else:
            not_found.append(f"{track['name']} by {track['artist']}")
            print(
                colored_text(
                    f" ╰─ Song number {spotify_tracks.index(track)+1} : {track['name']} by {track['artist']} was not found",
                    LRED,
                )
            )

    if apple_music_track_ids:
        print(colored_text(f"[+] Adding tracks to the Apple Music playlist", DGREY))
        create_apple_music_playlist(am_playlist_name, apple_music_track_ids)
    else:
        print(
            colored_text(
                "[-] No tracks were found on Apple Music, playlist not created", LRED
            )
        )
    
    if output:
        print(colored_text(f"[+] Creating output file", DGREY))
        with open("output.txt", 'w') as file:
            for line in not_found:
                file.write(line + "\n")
        print(colored_text(f" ╰─ Tracks not found written to output.txt", LGREEN))
        


if __name__ == "__main__":
    # Call parser to get arguments from CLI
    args = parser()
    spotify_playlist_url = args.url
    am_playlist_name = args.name
    output = args.output

    # Load env variables
    load_dotenv()

    # Spotify API credentials
    SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
    SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
    SPOTIFY_REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")

    # Apple Music API credentials
    APPLE_MUSIC_DEVELOPER_TOKEN = os.getenv("APPLE_MUSIC_DEVELOPER_TOKEN")
    APPLE_MUSIC_USER_TOKEN = os.getenv("APPLE_MUSIC_USER_TOKEN")

    # Create token for Spotipy
    token = SpotifyOAuth(
        username="enailis",
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET,
        redirect_uri=SPOTIFY_REDIRECT_URI,
        scope="playlist-read-private",
        show_dialog=True,
    )

    sp = spotipy.Spotify(auth_manager=token)

    transfer_playlist(sp, spotify_playlist_url, am_playlist_name, output)