class UGParser:
    @staticmethod
    def parse_chords(song_text):
        chords = set()
        split = song_text.split("[ch]")
        for substring in split:
            leading = substring.split("[")[0]
            if len(leading) < 6:
                chords.add(leading)
        chords = list(chords)
        chords.sort()
        return chords

    @staticmethod
    def clean_song_for_printing(song_text):
        header_split = song_text.split("[ch]",1)        #need to find a different start indicator
        if len(header_split) < 2:
            return song_text
        song_text = header_split[1]
        song_text = song_text.replace("[ch]", "").replace("[/ch]", "").replace("\r\n","\n")
        return song_text
