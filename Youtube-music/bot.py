from ts3 import TS3Server
from pydub import AudioSegment
from pydub.playback import play
import youtube_dl

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
                # Download the video audio and convert it to a playable format
                video_url = message.split(" ", 1)[1]
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                }
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    info_dict = ydl.extract_info(video_url, download=False)
                    audio_url = info_dict['url']
                    audio = AudioSegment.from_file(audio_url)
                
                # Play the audio in the TeamSpeak channel
                play(audio)
