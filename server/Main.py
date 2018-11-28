import server.dbloader as dbloader
from server.model.song_model import Song
import re
import os


def add_song_dialog():
    infile_path = input("Enter the path of a file with song data.")
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
        correct = input("\nAll chords should appear above in bold.\nDoes that look right? Y/n\n").lower()
        if re.match("y.*", correct):
            dbloader.store_song(song)
            print("Saved song")
            print("Your file may need reformatting. The format should be as follows:\n"
                  + "song name\n"
                  + "artist name\n"
                  + "album\n"
                  + "genre\n"
                  + "song chord sheet, with chords tagged. e.g. [ch]D7[/ch]")
        else:
            pass
    else:
        print("file not found")




def delete_song():
    pass


def select_song_for(action):
    pass


def edit_song(song):
    pass


def generate_songbook():
    pass


def show_song_menu():
    command = ""
    while not re.match("b.*", command):
        command = input("[A]dd song/[D]elete song/[E]dit song/[B]ack").lower()
        if re.match("a.*", command):
            add_song_dialog()
        elif re.match("d.*", command):
            delete_song()
        elif re.match("e.*", command):
            edit_song(select_song_for("editing"))
        else:
            print("not a valid command")


def print_book():
    pass


def show_book_menu():
    command = input("[N]ew book/[D]elete book/[E]dit book/[P]rint book/[B]ack")
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


while True:
    command = input("Manage: [S]ongs/[B]ooks, or [Q]uit").lower()
    if re.match("s.*", command):
        show_song_menu()
    if re.match("b.*", command):
        show_book_menu()
    if re.match("q.*", command):
        exit(0)