from server.model.chord_model import Chord

class Song():
    def __init__(self, data, is_restore=False):
        if is_restore:
            self.__dict__ = data
        else:
            self.rating = int(data['rating']) or 0
            self.favorite_count = int(data['favorites']) or 0
            self.views = int(data['views']) or 0
            self.votes = int(data['votes']) or 0
            self.song_name = data['song_name'] or ""
            self.artist = data['artist'] or ""
            self.url = data['url'] or ""
            self.raw_song_text = data['song'] or ""
            self.chords = {}
            self.parse_song(data['song'])

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

    def jsonable(self):
        rv = self.__dict__
        rv["__type__"] = "Song"
        return self.__dict__
