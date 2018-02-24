import Scraper
import sys

def parse_chords(song_text):
    chords = set()
    split = song_text.split("[ch]")
    for substring in split:
        leading = substring.split("[")[0]
        if len(leading) < 6:
            chords.add(leading)
    print(chords)
    return chords


class Song:
    chords = []

    def __init__(self, raw_song_data):
        self.chords = parse_chords(raw_song_data['song'])


song_data = Scraper.get_raw_song(sys.argv[1])
song = Song(song_data)
print(song_data['song'])
