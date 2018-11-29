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