# Spotify2AppleMusic

I created this to transfer my playlists from Spotify to Apple Music to finally have a good audio quality.

## Requirements

```sh
pip install -r requirements.txt
```

After that you'll need to create a developer account on both Spotify and Apple Music to request their respective API. This will cost you $99 thanks to Apple 🤡

### Spotify

You have to create a developer account on [Spotify's website](https://developer.spotify.com/) to use their API. Then go to your [dashboard](https://developer.spotify.com/dashboard) and create an app. You'll need to add the Client ID, the Secret ID and the Redirect URI to the `.env` file.

### Apple Music

To "protect against abusive use" of their API, Apple is restricting access to developer accounts which mean you'll have to pay $99.

Go to [Apple Developer website](https://developer.apple.com/), create an account and sub to the service. Once you've done this, you'll have to wait 24 to 48h to have your account approved. Then you'll be able to generate a token in `Certificates, Identifiers & Profiles > Identifiers`. You'll need to add the Developer Token and your User Token to the `.env` file.

## Usage

```
> python spotify2applemusic.py -h

usage: spotify2applemusic.py [-h] -url URL -name NAME [-o OUTPUT]

options:
  -h, --help            show this help message and exit
  -url URL, --spotify-playlist-url URL
                        Spotify playlist url
  -name NAME, --AM-playlist-name NAME
                        Apple Music name for the transfered playlist
  -o OUTPUT, --output OUTPUT
                        'True' if you want the songs not found to be written in a txt file, 'False' if not
```

By default, the "output" option is set to `False`. If you set this option to `True` but you already have an `output.txt` file, it will override its content.

## Disclaimer

I've done this project to switch from Spotify to Apple Music, this probably won't be maintained.
