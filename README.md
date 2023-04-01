
# Teamspeak Music Bot - SaM


This code connects to a TeamSpeak server running on "127.0.0.1:10011", logs in as the server admin with the given password, and joins channel ID "1". The while True loop keeps the bot running indefinitely.

This code loads an MP3 file named music.mp3 and plays it using PyDub's play() function. You can modify this code to load and play different music files as desired.

if a message is received that matches "!play", it loads and plays the music file. You can modify this code to add additional commands, error handling, and other functionality as needed.

Note that this is just a basic example to get you started. There are many ways you can extend and customize this bot to suit your needs, such as adding queue functionality, volume control, and more.


## Installation


To build a TeamSpeak music bot in Python, you can use the TeamSpeak 3 Python API library, along with a music playback library such as PyDub. Here's an example of how you can get started:

Install the necessary libraries:

```bash
  pip install teamspeak
  pip install PyDub
```


Make sure to replace the server address, login credentials, and music file name with the appropriate values for your own setup. You can run this script from the command line using "python bot.py" or by running it in an IDE like PyCharm.
