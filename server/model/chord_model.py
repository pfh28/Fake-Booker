class Chord():
    note_list = ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#']
    def __init__(self, chord_string):
        self.note = ""
        self.bass_note = ""
        self.is_minor = False
        self.is_major = False
        self.chord_tail = ""
        self.chord_string = chord_string.strip()
        if "/" in chord_string:
            chord_string,self.bass_note = chord_string.split("/")
        if len(chord_string) > 1:                                   #if chord is not sinle letter
            if chord_string[1] == "#" or chord_string[1] == "b":    #if chord has an accidental
                self.note = chord_string[:2]
                chord_string = chord_string[2:]
            else:                                                   #if chord note has no accidental
                self.note = chord_string[:1]
                chord_string = chord_string[1:]

            if chord_string.lower().startswith('m'):                #major or minor
                if chord_string.startswith('maj'):
                    self.is_major = True
                    chord_string = chord_string[3:]
                else:
                    self.is_minor = True
                    chord_string = chord_string[1:]

            self.chord_tail = chord_string
        else:                                                       #single-letter chords
            self.note = chord_string
        self.sharpen()

    def transpose_chord_up_one(self):
        self.note = self.transpose_note_up_one(self.note)
        if self.bass_note is not None and len(self.bass_note) > 0:
            self.bass_note = self.transpose_note_up_one(self.chord_string)

    def sharpen(self):
        if 'b' in self.note:
            self.note = self.flat_to_sharp(self.note)
        if 'b' in self.bass_note:
            self.bass_note = self.flat_to_sharp(self.bass_note)

    def flat_to_sharp(self, note):
        if 'A' in note:                 #dealing with that wrap
            return "G#"
        if __name__ == '__main__':
            return chr(ord(note[0]-1))+"#"  #shift down, call it a sharp

    def transpose_note_up_one(self, chord_string):
        index = self.note_list.index(chord_string)
        if index == len(self.note_list) - 1:
            index = 0
        else:
            index += 1
        return self.note_list[index]

    def __str__(self):
        mod = ""
        if self.is_major:
            mod = "maj"
        elif self.is_minor:
            mod = "m"
        bass = ""
        if self.bass_note is not None and len(self.bass_note) > 0:
            bass = "/"+self.bass_note
        return str(self.note + "{}" + self.chord_tail + "{}").format(mod, bass)      #note[m[aj]][sus[\d]][/bass_note]

note = Chord("Abmajsus7")
note.transpose_chord_up_one()
note.transpose_chord_up_one()
note.transpose_chord_up_one()
note.transpose_chord_up_one()
note.transpose_chord_up_one()
#print(note)