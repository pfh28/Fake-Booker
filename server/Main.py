import server.dbloader as dbloader
from server.model.song_model import Song
import re
import os

def ask_y_n(prompt):
    while True:             # loop until there's something to return
        response = input("{} Y/n\n".format(prompt))
        if re.match("y.*", response, re.IGNORECASE):
            return True
        elif re.match("n.*", response, re.IGNORECASE):
            return False
        else:
            print("Please enter [Y]es or [n]o\n")

def add_song_dialog():
    infile_path = input("Enter the path of a file with song data.\n")
    if os.path.isfile(infile_path):
        with open(infile_path, "r") as in_file:
            song_data = {}
            song_data['song_name'] = in_file.readline().strip()
            song_data['artist'] = in_file.readline().strip()
            song_data['album'] = in_file.readline().strip()
            song_data['genre'] = in_file.readline().strip()
            blank_count = 0             # loop terminates when two blank lines are read
            song_data['song_text'] = ""
            while blank_count < 2:
                line = in_file.readline()
                song_data['song_text'] += line
                if line == '':
                    blank_count += 1

        song = Song(song_data)
        print("\n"+song.song_name)
        print(song.artist)
        print(song.get_terminal_song_text())
        correct = ask_y_n("\nAll chords should appear above in bold.\nDoes that look right?")
        if correct:
            dbloader.store_song(song)
            print("Saved song")
        else:
            print("Your file may need reformatting. The format should be as follows:\n"
                  + "song name\n"
                  + "artist name\n"
                  + "album\n"
                  + "genre\n"
                  + "song chord sheet, with chords tagged. e.g. [ch]D7[/ch]")
    else:
        print("file not found")


def delete_song(song):
    if ask_y_n("are you sure you want to delete {}".format(song.song_name)):
        dbloader.delete_song(song)
        print("deleted {}\n".format(song.song_name))
    else:
        print("cancelled delete")


def select_song_for(action):
    print("find a song to {}".format(action))
    print("Fill the fields, leave blank to ignore")
    features = {'song_name': "Song Title", 'artist': "Artist", 'album': "Album", 'genre': "Genre"}  # search features
    for k, v in features.items():       # hacky, but I'm using the initial values as prompts.
        features[k] = re.compile(".*" + input(v + ": ") + ".*", re.IGNORECASE)
    songs = dbloader.get_songs_matching(features)
    for i in range(len(songs)):
        print(str(i+1) + " \t" + songs[i].song_name)
    selection = input("\nselect a song number. 0 to go back.")
    if selection.isdigit() and 0 < int(selection) <= len(songs):    # if a valid index is selected
        return songs[int(selection) - 1]
    else:
        return None

def edit_song(song):
    pass


def generate_songbook():
    pass


def show_song_menu():
    command = ""
    while not re.match("b.*", command):
        command = input("[A]dd song/[D]elete song/[E]dit song/[B]ack\n").lower()
        if re.match("a.*", command):
            add_song_dialog()
        elif re.match("d.*", command):
            song = select_song_for("delete")
            if song is None:
                continue
            delete_song(song)
        elif re.match("e.*", command):
            song = select_song_for("edit")
            if song is None:
                continue
            edit_song(song)
        else:
            print("not a valid command")


def print_book():
    pass


def show_book_menu():
    command = input("[N]ew book/[D]elete book/[E]dit book/[P]rint book/[B]ack\n")
    command = command.lower()
    if re.match("n.*", command):
        add_song_dialog()
    elif re.match("d.*", command):
        delete_song()
    elif re.match("e.*", command):
        edit_song()
    elif re.match("p.*", command):
        print_book()
    elif re.match("b.*", command):
        return
    else:
        print("not a valid command")

# select_song_for("test")
while True:
    command = input("Manage: [S]ongs/[B]ooks, or [Q]uit\n").lower()
    if re.match("s.*", command):
        show_song_menu()
    if re.match("b.*", command):
        show_book_menu()
    if re.match("q.*", command):
        exit(0)
