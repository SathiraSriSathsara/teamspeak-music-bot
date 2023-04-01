from ts3 import TS3Server
from pydub import AudioSegment
from pydub.playback import play
import youtube_dl
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Set up the Spotify API credentials
client_id = 'YOUR_CLIENT_ID'
client_secret = 'YOUR_CLIENT_SECRET'
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Connect to the TeamSpeak server
ts = TS3Server("127.0.0.1", 10011)
ts.login("serveradmin", "password")
ts.use(1)
ts.clientmove(cid=1, clid=ts.whoami()['client_id'])

# Wait for incoming events
while True:
    events = ts.wait_for_event()
    for event in events:
        if event[0]['reasonid'] == 'reasonmsg':
            message = event[0]['msg']
            if message.startswith("!play "):
                # Check if the URL is a Spotify track or playlist
                url = message.split(" ", 1)[1]
                if 'track' in url:
                    track_id = url.split("/")[-1]
                    track = sp.track(track_id)
                    audio_url = track['preview_url']
                elif 'playlist' in url:
                    playlist_id = url.split("/")[-1]
                    results = sp.playlist(playlist_id, fields="tracks")
                    tracks = results['tracks']['items']
                    audio_url = tracks[0]['track']['preview_url']
                else:
                    continue
                
                # Download the audio and convert it to a playable format
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                }
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    audio = AudioSegment.from_file(audio_url)
                
                # Play the audio in the TeamSpeak channel
                play(audio)
