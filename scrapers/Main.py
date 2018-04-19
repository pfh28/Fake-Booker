import sys

from scrapers import SongProcessor

songs = []
with open(sys.argv[1], "r") as in_file:
    for line in in_file:
        song = SongProcessor.song_from_url(line)
        if song is not None:
            songs.append(song)

with open("out.txt", "w") as out_file:
    for song in songs:
        print(song.title)
        out_file.write(str(song))
        out_file.write("\n"+"_"*80+"\n")
