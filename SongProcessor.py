import Scraper
import sys
import songparsers


class Song:
    def __init__(self, raw_song_data, parser):
        self.chords = parser.parse_chords(raw_song_data['song'])
        self.cleaned_song_text = parser.clean_song_for_printing(raw_song_data['song'])
        self.title = raw_song_data['song_name']
        self.artist = raw_song_data['artist']

    def __str__(self):
        rv = self.title + " by " + self.artist + "\n" + str(self.chords) + "\n\n" + self.cleaned_song_text
        return rv

#song_data = Scraper.get_raw_song(sys.argv[1])
#song = Song(song_data, songparsers.UGParser)
#print(song)
def song_from_url(url):
    song_data = Scraper.get_raw_song(url)
    if song_data is None:
        return None
    song = Song(song_data, songparsers.UGParser)
    if len(song.chords) == 0:
        print(url)
        return None
    return song
