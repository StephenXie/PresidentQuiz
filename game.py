import curses
import time
from curses.textpad import Textbox, rectangle
import pyautogui
WIN_X, WIN_Y = 10, 10
presidents = []
title_art = "  ____                _     _            _     _     _     _   \n |  _ \ _ __ ___  ___(_) __| | ___ _ __ | |_  | |   (_)___| |_  \n | |_) | '__/ _ \/ __| |/ _` |/ _ \ '_ \| __| | |   | / __| __| \n |  __/| | |  __/\__ \ | (_| |  __/ | | | |_  | |___| \__ \ |_  \n |_|   |_|  \___||___/_|\__,_|\___|_| |_|\__| |_____|_|___/\__| \n                                                              "
last_names = []
last_name_to_president = {}
current_score = 0
current_guesses = {}
with open("presidents.txt", "r") as reader:
    N = 0
    for line in reader:
        line = line.replace("\n","")
        last_name = line.split(" ")[-1]
        presidents.append([line, last_name])
        last_names.append(last_name.lower())
        if last_name.lower() in last_name_to_president:
            last_name_to_president[last_name.lower()].append(line)
        else:
            last_name_to_president[last_name.lower()] = [line]
        
        current_guesses[line] = False
        N+=1




def add_column(stdscr, text, X, Y, n):
    spacing = 1
    n+=1
    for i in range(len(text)):
        if current_guesses[text[i][0]]:
            stdscr.addstr((Y+i*spacing),X,str(n) + ". " + text[i][0])
        else:
            stdscr.addstr((Y+i*spacing),X,str(n) + ". ")
        n+=1
    stdscr.refresh()

def columns(stdscr):
    Y = WIN_Y//4
    # left column
    X = 2*WIN_X//8
    add_column(stdscr, presidents[:N//2+1], X, Y, 0)
    # right column
    X = 5*WIN_X//8
    add_column(stdscr, presidents[N//2+1:], X, Y, N//2+1)

def draw_title(stdscr):
    n = 0
    for i in title_art.split("\n"):
        print(i)
        stdscr.addstr(n, WIN_X//4, i)
        n+=1
    

def home(stdscr):
    global WIN_Y
    global WIN_X
    cur_key = 0
    while True:
        if cur_key==0:
            pyautogui.press('enter')
        # if cur_key == curses.KEY_RESIZE:
        #     WIN_Y, WIN_X = stdscr.getmaxyx()
        #     stdscr.clear()
        #     stdscr.refresh()
        # if cur_key == 27 or cur_key == curses.KEY_COPY or cur_key == curses.KEY_END or cur_key == curses.KEY_BREAK:
        #     return
        # # stdscr.clear()
        
        if text_box(stdscr):
            return
        columns(stdscr)
        draw_title(stdscr)
        stdscr.addstr(5, 2*WIN_X//3, "Score: " + str(current_score))
        stdscr.refresh()
        if current_score >= N:
            game_over(stdscr)
            return
        cur_key+=1
        
def validator(text):
    if text == 10:
        return 7
    else:
        return text

def game_over(stdscr):
    stdscr.clear()
    stdscr.addstr(WIN_Y//2, WIN_X//2, "Congrats!")
    stdscr.refresh()
    time.sleep(5)
    return
def text_box(stdscr):
    global current_score
    global current_guesses
    BOX_W = 60
    BOX_H = 4
    editwin = curses.newwin(BOX_H, BOX_W, 35, WIN_X//2 - BOX_W//2)
    rectangle(stdscr, 35 - 1, WIN_X//2 - BOX_W//2 - 1, 35 + BOX_H, WIN_X//2 + BOX_W//2)
    box = Textbox(editwin)
    # pyautogui.press(chr(cur_key +  ord("a")))
    box.edit(validator)
    message = box.gather().strip().lower()
    print(message)
    if message == "quit":
        return True
    if message in last_names:
        matching_presidents = last_name_to_president[message]
        for president in matching_presidents:
            current_guesses[president] = True
            current_score+=1
    

def set_colors(stdscr):
    if curses.has_colors():
        curses.use_default_colors()
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)

def main(stdscr):
    global WIN_X
    global WIN_Y
    WIN_Y, WIN_X = stdscr.getmaxyx()
    curses.curs_set(False)
    set_colors(stdscr)
    stdscr.scrollok(True)
    curses.resize_term(45,120)
    home(stdscr)
print(last_names)
curses.wrapper(main)