import uuid


class SongBook():
    def __init__(self, book_title, preferred_chords):
        self.title = book_title
        self.preferred_chords = preferred_chords
        self.songs = []
        self._id = str(uuid.uuid4())

    def set_title(self, book_title):
        self.title = book_title

    def set_preferred_chords(self, preferred_chords):
        self.preferred_chords = preferred_chords

    def add_song(self, song):
        self.songs.append(song)

    def get_details(self):
        rv = self.title + "\n" + "Preferred Chords: "
        for chord in self.preferred_chords:
            rv += str(chord) + " "
        rv += "\n\nSongs:\n"
        for song in self.songs:
            rv += song.song_name + "\n"
        return rv

    def jsonable(self):
        rv = self.__dict__
        rv["__type__"] = "SongBook"
        songs = []
        for song in rv['songs']:        # only store song ids with book
            songs.append(song._id)
        rv['songs'] = songs
        return rv
