from server.model.chord_model import Chord

class Song():
    def __init__(self, raw_song_data, url):
        self.rating = int(raw_song_data['rating']) or 0
        self.favorite_count = int(raw_song_data['favorites']) or 0
        self.views = int(raw_song_data['views']) or 0
        self.votes = int(raw_song_data['votes']) or 0
        self.song_name = raw_song_data['song_name'] or ""
        self.artist = raw_song_data['artist'] or ""
        self.raw_song_text = raw_song_data['song'] or ""
        self.chords = {}
        self.parse_song(raw_song_data['song'])

    def parse_song(self, song_text):
        song_parts = song_text.split("[ch]")                    # split into sections starting with a chord
        song_parts = song_parts[1:]
        for part in song_parts:
            chord_string = part.split("[/ch]")[0].strip()       # get chord string
            if chord_string not in self.chords.keys():          # if this chord hasn't appeared in this song before
                self.chords[chord_string] = Chord(chord_string) # create and store the chord object

    def transpose_up_one(self):
        for chord in self.chords.values():
            chord.transpose_chord_up_one()

    def get_song_text(self):
        rv = self.raw_song_text
        for chord_string, chord in self.chords.items():
            rv = rv.replace("[ch]" + chord_string + "[/ch]", str(chord))    # str(chord) prints the transposed chord
        return rv