import curses, json, datetime
from ciphers import *


def get_data():
    with open("db.json", "r") as f:
        data = json.loads(f.read())
    return data


def save_data(data):
    with open("db.json", "w") as f:
        f.write(json.dumps(data))


def save_encoding(cipher_type, plaintext, ciphertext):
    data = get_data()
    max_id = -1
    for e in data:
        if e['id'] > max_id:
            max_id = e['id']
    data.append({"id": max_id + 1, "cipher_type": cipher_type, "plaintext": plaintext, "ciphertext": ciphertext})
    save_data(data)
    with open("output.txt", "w") as f:
        f.write("cipher type: {}\nplaintext: {}\nciphertext: {}\ndate: {}".format(cipher_type, plaintext, ciphertext,
                                                                                  datetime.datetime.now().strftime(
                                                                                      "%Y-%m-%d %H:%M:%S")))


def display_input(stdscr, greeting_string, end_string):
    stdscr.clear()
    stdscr.border(0)
    stdscr.addstr(1, 1, greeting_string)
    stdscr.addstr(4, 1, end_string)
    text = ""
    while True:
        key = stdscr.getch()
        if key in [curses.KEY_ENTER, ord("\n")]:
            stdscr.clear()
            stdscr.border(0)
            return text
        elif key in [curses.KEY_BACKSPACE, ord('\b')]:
            stdscr.clear()
            stdscr.border(0)
            text = text[:-1]
            stdscr.addstr(1, 1, greeting_string)
            stdscr.addstr(4, 1, end_string)
            stdscr.addstr(2, 1, text)
        else:
            text += chr(key)
            stdscr.addstr(2, 1, text)

def display_password_input(stdscr, greeting_string, end_string):
    stdscr.clear()
    stdscr.border(0)
    stdscr.addstr(1, 1, greeting_string)
    stdscr.addstr(4, 1, end_string)
    text = ""
    passtext = ""
    while True:
        key = stdscr.getch()
        if key in [curses.KEY_ENTER, ord("\n")]:
            stdscr.clear()
            stdscr.border(0)
            return text
        elif key in [curses.KEY_BACKSPACE, ord('\b')]:
            stdscr.clear()
            stdscr.border(0)
            text = text[:-1]
            passtext = passtext[:-1]
            stdscr.addstr(1, 1, greeting_string)
            stdscr.addstr(4, 1, end_string)
            stdscr.addstr(2, 1, passtext)
        else:
            text += chr(key)
            passtext += "*"
            stdscr.addstr(2, 1, passtext)

def display_encoding(stdscr, plaintext, ciphertext):
    stdscr.clear()
    stdscr.border(0)
    stdscr.addstr(1, 1, "Here's data you provided us with. Remember, data also saved in db.json and output.txt files.")
    stdscr.addstr(2, 1, "Plaintext: {}".format(plaintext))
    stdscr.addstr(3, 1, "Ciphertext: {}".format(ciphertext))
    stdscr.addstr(4, 1, "Press enter to continue...")
    while True:
        key = stdscr.getch()
        if key in [curses.KEY_ENTER, ord("\n")]:
            stdscr.clear()
            stdscr.border(0)
            return text

# def display_menu(stdscr, items):
#     stdscr = curses.initscr()
#     curses.noecho()
#     curses.cbreak()
#     stdscr.keypad(1)
#     stdscr.border(0)
#     curses.curs_set(0)

if __name__ == "__main__":
    try:
        # -- Initialize --
        stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        stdscr.keypad(1)
        stdscr.border(0)
        # stdscr.addstr(5, 5, 'Hello from Curses!', curses.A_BOLD)
        # stdscr.addstr(6, 5, 'Press q to close this screen', curses.A_NORMAL)

        curses.curs_set(0)
        # -- Main Loop --
        items = [
            ["Encode using available ciphers", "encode"],
            ["Decode using available ciphers", "decode"],
            ["Exit"]
        ]
        cipher_items = [
            ["Caesar", curses.beep],
            ["Gronsfeld", curses.beep],
            ["Polibius", curses.beep],
            ["XOR", curses.beep],
            ["Atbash", curses.beep],
            ["Return"]
        ]
        position = 0
        password = display_password_input(stdscr, "Welcome, please enter a password to continue:",
                                          "if you forgot your password, then look in the code.")
        if password == "password":
            while True:
                stdscr.addstr(1, 1, "Welcome to main menu. Choose the option needed.")
                for index, item in enumerate(items):
                    if index == position:
                        mode = curses.A_REVERSE
                    else:
                        mode = curses.A_NORMAL
                    stdscr.addstr(3 + index * 2, 2, "{}".format(item[0]), mode)

                key = stdscr.getch()

                if key == ord('q'):
                    break
                elif key == curses.KEY_UP:
                    position -= 1
                    if position < 0:
                        position = len(items) - 1
                elif key == curses.KEY_DOWN:
                    position += 1
                    if position >= len(items):
                        position = 0

                elif key in [curses.KEY_ENTER, ord("\n")]:
                    if position == len(items) - 1:  # last item in menu is exit
                        break
                    elif items[position][1] == "encode":
                        stdscr.clear()
                        stdscr.border(0)
                        position = 0
                        while True:
                            stdscr.addstr(1, 1, "Which cipher would you like to use?")
                            for index, item in enumerate(cipher_items):
                                if index == position:
                                    mode = curses.A_REVERSE
                                else:
                                    mode = curses.A_NORMAL
                                if index != len(cipher_items) - 1:
                                    stdscr.addstr(3 + index * 2, 2, "{}. {}".format(1 + index, item[0]), mode)
                                else:
                                    stdscr.addstr(3 + index * 2, 2, "{}".format(item[0]), mode)
                            key = stdscr.getch()
                            if key == ord('q'):
                                break
                            elif key == curses.KEY_UP:
                                position -= 1
                                if position < 0:
                                    position = len(cipher_items) - 1
                            elif key == curses.KEY_DOWN:
                                position += 1
                                if position >= len(cipher_items):
                                    position = 0
                            elif key in [curses.KEY_ENTER, ord("\n")]:
                                if position == len(cipher_items) - 1:  # last item in menu is exit
                                    stdscr.clear()
                                    stdscr.border(0)
                                    position = 0
                                    break
                                elif cipher_items[position][0] == "Caesar":
                                    plaintext = display_input(stdscr,
                                                              "Please, enter string you want to encode, using Caesar cipher:",
                                                              "We will save your ciphertext in the 'database' as well as in the file output.txt")
                                    key = display_input(stdscr, "Please, enter a integer key:",
                                                        "We will save your ciphertext in the 'database' as well as in the file output.txt")
                                    try:
                                        ciphertext = caesar_encode(plaintext, int(key))
                                        save_encoding("caesar", plaintext, ciphertext)
                                        display_encoding(stdscr, plaintext, ciphertext)
                                    except:
                                        pass
                                elif cipher_items[position][0] == "Gronsfeld":
                                    plaintext = display_input(stdscr,
                                                              "Please, enter string you want to encode, using Gronsfeld cipher:",
                                                              "We will save your ciphertext in the 'database' as well as in the file output.txt")
                                    key = display_input(stdscr, "Please, enter a integer key:",
                                                        "We will save your ciphertext in the 'database' as well as in the file output.txt")
                                    try:
                                        ciphertext = gronsfeld_encode(plaintext, int(key))
                                        save_encoding("gronsfeld", plaintext, ciphertext)
                                        display_encoding(stdscr, plaintext, ciphertext)
                                    except:
                                        pass
                                elif cipher_items[position][0] == "Polibius":
                                    plaintext = display_input(stdscr,
                                                              "Please, enter string you want to encode, using Polibius cipher:",
                                                              "We will save your ciphertext in the 'database' as well as in the file output.txt")
                                    key = display_input(stdscr, "Please, enter a integer key:",
                                                        "We will save your ciphertext in the 'database' as well as in the file output.txt")
                                    try:
                                        ciphertext = polibius_encode(plaintext)
                                        save_encoding("polibius", plaintext, ciphertext)
                                        display_encoding(stdscr, plaintext, ciphertext)
                                    except:
                                        pass
                                elif cipher_items[position][0] == "XOR":
                                    plaintext = display_input(stdscr,
                                                              "Please, enter string you want to encode, using XOR cipher:",
                                                              "We will save your ciphertext in the 'database' as well as in the file output.txt")
                                    key = display_input(stdscr, "Please, enter a key:",
                                                        "We will save your ciphertext in the 'database' as well as in the file output.txt")
                                    try:
                                        ciphertext = xor_encode(plaintext, key)
                                        save_encoding("XOR", plaintext, ciphertext)
                                        display_encoding(stdscr, plaintext, ciphertext)
                                    except:
                                        pass
                                elif cipher_items[position][0] == "Atbash":
                                    plaintext = display_input(stdscr,
                                                              "Please, enter string you want to encode, using Atbash cipher:",
                                                              "We will save your ciphertext in the 'database' as well as in the file output.txt")
                                    try:
                                        ciphertext = atbash_encode(plaintext)
                                        save_encoding("atbash", plaintext, ciphertext)
                                        display_encoding(stdscr, plaintext, ciphertext)
                                    except:
                                        pass
                    elif items[position][1] == "decode":
                        stdscr.clear()
                        stdscr.border(0)
                        position = 0
                        while True:
                            stdscr.addstr(1, 1, "Which cipher would you like to use?")
                            for index, item in enumerate(cipher_items):
                                if index == position:
                                    mode = curses.A_REVERSE
                                else:
                                    mode = curses.A_NORMAL
                                if index != len(cipher_items) - 1:
                                    stdscr.addstr(3 + index * 2, 2, "{}. {}".format(1 + index, item[0]), mode)
                                else:
                                    stdscr.addstr(3 + index * 2, 2, "{}".format(item[0]), mode)
                            key = stdscr.getch()
                            if key == ord('q'):
                                break
                            elif key == curses.KEY_UP:
                                position -= 1
                                if position < 0:
                                    position = len(cipher_items) - 1
                            elif key == curses.KEY_DOWN:
                                position += 1
                                if position >= len(cipher_items):
                                    position = 0
                            elif key in [curses.KEY_ENTER, ord("\n")]:
                                if position == len(cipher_items) - 1:  # last item in menu is exit
                                    stdscr.clear()
                                    stdscr.border(0)
                                    position = 0
                                    break
                                elif cipher_items[position][0] == "Caesar":
                                    ciphertext = display_input(stdscr,
                                                               "Please, enter string you want to decode, using Caesar cipher:",
                                                               "We will save your ciphertext in the 'database' as well as in the file output.txt")
                                    key = display_input(stdscr, "Please, enter a integer key:",
                                                        "We will save your ciphertext in the 'database' as well as in the file output.txt")
                                    try:
                                        plaintext = caesar_decode(ciphertext, int(key))
                                        save_encoding("caesar", plaintext, ciphertext)
                                        display_encoding(stdscr, plaintext, ciphertext)
                                    except:
                                        pass
                                elif cipher_items[position][0] == "Gronsfeld":
                                    ciphertext = display_input(stdscr,
                                                               "Please, enter string you want to decode, using Gronsfeld cipher:",
                                                               "We will save your ciphertext in the 'database' as well as in the file output.txt")
                                    key = display_input(stdscr, "Please, enter a integer key:",
                                                        "We will save your ciphertext in the 'database' as well as in the file output.txt")
                                    try:
                                        plaintext = gronsfeld_decode(ciphertext, int(key))
                                        save_encoding("gronsfeld", plaintext, ciphertext)
                                        display_encoding(stdscr, plaintext, ciphertext)
                                    except:
                                        pass
                                elif cipher_items[position][0] == "Polibius":
                                    ciphertext = display_input(stdscr,
                                                               "Please, enter string you want to decode, using Polibius cipher:",
                                                               "We will save your ciphertext in the 'database' as well as in the file output.txt")
                                    key = display_input(stdscr, "Please, enter a integer key:",
                                                        "We will save your ciphertext in the 'database' as well as in the file output.txt")
                                    try:
                                        plaintext = polibius_decode(ciphertext)
                                        save_encoding("polibius", plaintext, ciphertext)
                                        display_encoding(stdscr, plaintext, ciphertext)
                                    except:
                                        pass
                                elif cipher_items[position][0] == "XOR":
                                    ciphertext = display_input(stdscr,
                                                               "Please, enter string you want to decode, using XOR cipher:",
                                                               "We will save your ciphertext in the 'database' as well as in the file output.txt")
                                    key = display_input(stdscr, "Please, enter a key:",
                                                        "We will save your ciphertext in the 'database' as well as in the file output.txt")
                                    try:
                                        plaintext = xor_decode(ciphertext, key)
                                        save_encoding("XOR", plaintext, ciphertext)
                                        display_encoding(stdscr, plaintext, ciphertext)
                                    except:
                                        pass
                                elif cipher_items[position][0] == "Atbash":
                                    ciphertext = display_input(stdscr,
                                                               "Please, enter string you want to decode, using Atbash cipher:",
                                                               "We will save your ciphertext in the 'database' as well as in the file output.txt")
                                    try:
                                        plaintext = atbash_decode(ciphertext)
                                        save_encoding("atbash", plaintext, ciphertext)
                                        display_encoding(stdscr, plaintext, ciphertext)
                                    except:
                                        pass
                    else:
                        items[position][1]()


    except:
        pass
    
    finally:
        # --- Cleanup on exit ---
        stdscr.keypad(0)
        curses.echo()
        curses.nocbreak()
        curses.endwin()
