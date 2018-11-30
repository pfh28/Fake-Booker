import re


def ask_y_n(prompt):
    while True:             # loop until there's something to return
        response = input("{} Y/n\n".format(prompt))
        if re.match("y.*", response, re.IGNORECASE):
            return True
        elif re.match("n.*", response, re.IGNORECASE):
            return False
        else:
            print("Please enter [Y]es or [n]o\n")

def select_song(songs):
    for i in range(len(songs)):
        print(str(i+1) + " \t" + songs[i].song_name)
    selection = input("\nselect a song number. 0 to go back.")
    if selection.isdigit() and 0 < int(selection) <= len(songs):    # if a valid index is selected
        return songs[int(selection) - 1]
    else:
        return None