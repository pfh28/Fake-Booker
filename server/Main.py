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


def print_song(song):
    print("\n" + song.song_name)
    print(song.artist)
    print(song.get_terminal_song_text())


def save_song_dialog(song, message=""):
    print_song(song)
    print(message)
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


def read_song_from_file(path):
    with open(path, "r") as in_file:
        song_data = {}
        song_data['song_name'] = in_file.readline().strip()
        song_data['artist'] = in_file.readline().strip()
        song_data['album'] = in_file.readline().strip()
        song_data['genre'] = in_file.readline().strip()
        blank_count = 0  # loop terminates when two blank lines are read
        song_data['song_text'] = ""
        while blank_count < 2:
            line = in_file.readline()
            song_data['song_text'] += line
            if line == '':
                blank_count += 1
    return Song(song_data)


def add_song_dialog():
    infile_path = input("Enter the path of a file with song data.\n")
    if os.path.isfile(infile_path):
        song = read_song_from_file(infile_path)
        save_song_dialog(song)
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


def edit_song(song):                                    # song is written to a file for editing
    edit_file_path = "{}{}.txt".format(song.song_name, song._id).replace(" ", "_")
    if os.path.isfile(edit_file_path):                  # if the file exists, read it in
        song = read_song_from_file(edit_file_path)
        song._id = song._id
        save_song_dialog(song, "it looks like you've edited this song")
    else:                                               # if it doesn't, write it
        with open(edit_file_path, "w") as out_file:
            out_file.write(song.song_name + "\n")
            out_file.write(song.artist + "\n")
            out_file.write(song.album + "\n")
            out_file.write(song.genre + "\n")
            out_file.write(song.raw_song_text)
        print("\nThe song details are written in {}.\n".format(edit_file_path)
              + "Edit the file, and then select this song again for editing to save your changes.\n")


def generate_songbook():
    pass


def show_song_menu():
    command = ""
    while True:
        command = input("[A]dd song/[D]elete song/[E]dit song/[V]iew song/[B]ack\n").lower()
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
        elif re.match("v.*", command):
            song = select_song_for("view")
            if song is None:
                continue
            print_song(song)
        elif re.match("b.*", command):
            return
        else:
            print("not a valid command")


def print_book():
    pass


def show_book_menu():
    command = input("[N]ew book/[D]elete book/[E]dit book/[P]rint book/[V]iew book/[B]ack\n")
    command = command.lower()
    if re.match("n.*", command):
        add_song_dialog()
    elif re.match("d.*", command):
        delete_song()
    elif re.match("e.*", command):
        edit_song()
    elif re.match("p.*", command):
        print_book()
    elif re.match("v.*", command):
        print_book()
    elif re.match("b.*", command):
        return
    else:
        print("not a valid command")


while True:
    command = input("Manage: [S]ongs/[B]ooks, or [Q]uit\n").lower()
    if re.match("s.*", command):
        show_song_menu()
    if re.match("b.*", command):
        show_book_menu()
    if re.match("q.*", command):
        exit(0)
