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


def select_book_for(action):
    print("Pick a book to {}".format(action))
    books = dbloader.get_book_list()
    for i in range(len(books)):
        print(str(i+1) + " \t" + books[i].title)
    selection = input("\nselect a song number. 0 to go back.")
    if selection.isdigit() and 0 < int(selection) <= len(books):    # if a valid index is selected
        return books[int(selection) - 1]
    else:
        return None


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
        song = select_song_for("add")
        if song is not None:
            book.add_song(song)
        if not ask_y_n("Add another song?"):
            return


def add_book_dialog():
    title = force_get_string("Set songbook title.")
    print("Add your preferred chords")
    chords = collect_chords()
    book = SongBook(title, chords)
    add_songs(book)
    dbloader.store_book(book)


def view_book(book):
    print(book.get_details())


def delete_book(book):
    if ask_y_n("Are you sure you want to delete {}?".format(book.title)):
        dbloader.delete_book(book)
        print("Deleted {}.".format(book.title))


def remove_songs(book):
    while True:
        if len(book.songs) == 0:
            print("No more songs to remove")
            return
        print("\nSelect a song to remove.\n")
        book.remove_song(select_song(book.songs))
        if not ask_y_n("Remove another song from {}?".format(book.title)):
            return


def edit_book_dialog(book):
    while True:
        view_book(book)
        command = input("Update [T]itle/[P]referred chords/[A]dd Songs/[R]emove Songs/[F]inish\n").lower()
        if re.match("t.*", command):
            book.title = force_get_string("Set songbook title.")
        elif re.match("p.*", command):
            print("Resetting selected chords.")
            book.preferred_chords = collect_chords()
        elif re.match("a.*", command):
            add_songs(book)
        elif re.match("r.*", command):
            remove_songs(book)
        elif re.match("f.*", command):
            if ask_y_n("Save changes to {}?".format(book.title)):
                dbloader.replace_book(book)
                print("replaced book")
            else:
                print("cancelled")
            return


def show_book_menu():
    while True:
        command = input("[N]ew book/[D]elete book/[E]dit book/[P]rint book/[V]iew book/[B]ack\n")
        command = command.lower()
        if re.match("n.*", command):
            add_book_dialog()
        elif re.match("d.*", command):
            book = select_book_for("delete")
            if book is None:
                continue
            delete_book(book)
        elif re.match("e.*", command):
            book = select_book_for("edit")
            if book is None:
                continue
            edit_book_dialog(book)
        elif re.match("p.*", command):
            print_book()
        elif re.match("v.*", command):
            book = select_book_for("view")
            if book is None:
                continue
            view_book(book)
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
