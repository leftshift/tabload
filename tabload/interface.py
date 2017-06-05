import curses
import itertools

from tabload import result_view


def _init(screen):
    curses.start_color()
    curses.use_default_colors()
    screen.keypad(True)
    screen.clear()

def main(screen, search):
    _init(screen)
    global height, width
    height, width = screen.getmaxyx()

    w_results = screen.subwin(height, width, 0,0)

    r_view = result_view.ResultView(w_results, search)

    if not r_view.display_page(0):
        pass  # handle no results

    while True:
        k = screen.getkey()
        if k == 'n':
            r_view.next_page()
        if k == 'p':
            r_view.prev_page()
        if k == 'KEY_UP':
            r_view.prev_item()
        if k == 'KEY_DOWN':
            r_view.next_item()
        if k == "KEY_ENTER" or k == " ":
            tab = r_view.get_curr_item()
            print(tab)
        if k == 'q':
            break


def display_results(search):
    curses.wrapper(main, search)
