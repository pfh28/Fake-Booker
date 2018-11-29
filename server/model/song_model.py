from server.model.chord_model import Chord
import uuid

class Song():
    def __init__(self, data, is_restore=False):
        if is_restore:
            self.__dict__ = data
        else:
            self.song_name = data['song_name'] or ""
            self.artist = data['artist'] or ""
            self.genre = "" #data['genre'] or ""
            self.album = "" #data['album'] or ""
            self.raw_song_text = data['song_text'] or ""
            self.chords = {}
            self._id = str(uuid.uuid4())
            self.parse_song(data['song_text'])

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

    def get_terminal_song_text(self):
        rv = self.raw_song_text
        for chord_string, chord in self.chords.items():
            rv = rv.replace("[ch]" + chord_string + "[/ch]", '\033[1m'+str(chord)+'\033[0m')    # print chords bolded
        return rv

    def jsonable(self):
        rv = self.__dict__
        rv["__type__"] = "Song"
        return self.__dict__
