import server.dbloader as dbloader
from server.model.song_model import Song
import re
import os
from server.utils import ask_y_n
from server.song_dialogs import *




def generate_songbook():
    pass


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
