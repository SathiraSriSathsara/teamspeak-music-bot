from ts3 import TS3Server
from pydub import AudioSegment
from pydub.playback import play

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
            if message == "!play":
                # Load and play the music file
                audio = AudioSegment.from_file("music.mp3", format="mp3")
                play(audio)
