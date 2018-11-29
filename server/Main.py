import server.dbloader as dbloader
from server.model.book_model import SongBook
from server.model.chord_model import Chord
from server.model.song_model import Song
import re
import os
from server.utils import ask_y_n
from server.song_dialogs import *


def force_get_string(prompt):
    rv = ''
    while len(rv) == 0:
        rv = input(prompt + "\nMay not be left blank.\n").strip()
    return rv





def collect_chords():
    chords = set()
    while True:
        chord_symbol = input("\nAdd chord. Use uppercase, use 'b' and '#' for sharp and flat.\n"
                            + "write 'done' to finish.\n").strip()
        if re.match(".*done.*", chord_symbol):
            return list(chords)
        elif Chord.looks_like_chord(chord_symbol):
            chords.add(Chord(chord_symbol))
        else:
            print("that doesn't look like a chord symbol")


def generate_songbook():
    pass


def print_book():
    pass


def add_songs(book):
    while True:
        book.add_song(select_song_for("add"))
        if not ask_y_n("Add another song?"):
            return


def add_book_dialog():
    title = force_get_string("Set songbook title.")
    print("Add your preferred chords")
    chords = collect_chords()
    book = SongBook(title, chords)
    add_songs(book)
    dbloader.store_book(book)



def show_book_menu():
    command = input("[N]ew book/[D]elete book/[E]dit book/[P]rint book/[V]iew book/[B]ack\n")
    command = command.lower()
    if re.match("n.*", command):
        add_book_dialog()
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
