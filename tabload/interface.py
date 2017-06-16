import curses
import itertools

from tabload import result_view, tab_view
from tabload import utils


tip_results = "Arrow keys: Select result\tEnter/Space: Select\tn/p: next/prev page\tq: quit"
tip_tab = "Arrow keys: Scroll\tBackspace: Return to results"

def _init(screen):
    curses.curs_set(0)
    curses.start_color()
    curses.use_default_colors()
    screen.keypad(True)
    screen.clear()

def show_tooltip(window, text):
    window.clear()
    window.insstr(text, curses.A_DIM)
    window.refresh()

def main(screen, search):
    _init(screen)
    global height, width
    height, width = screen.getmaxyx()

    w_results = screen.subwin(height-1, width, 0,0)
    w_tips = screen.subwin(1,width, height-1,0)

    show_tooltip(w_tips, "Loading…")

    r_view = result_view.ResultView(w_results, search)

    if not r_view.display_page(0):
        pass  # handle no results

    show_tooltip(w_tips, tip_results)

    while True:
        k = screen.getkey()
        if k == 'n':
            show_tooltip(w_tips, "Loading…")
            r_view.next_page()
            show_tooltip(w_tips, tip_results)
        if k == 'p':
            show_tooltip(w_tips, "Loading…")
            r_view.prev_page()
            show_tooltip(w_tips, tip_results)
        if k == 'KEY_UP':
            r_view.prev_item()
        if k == 'KEY_DOWN':
            r_view.next_item()
        if k in ("KEY_ENTER", " ", "\n", "\r"):
            tab = r_view.get_curr_item()
            t_view = tab_view.TabView(w_results, tab)
            t_view.show()
            show_tooltip(w_tips, tip_tab)
            while True:
                l = screen.getkey()
                if l == 'KEY_UP':
                    t_view.scroll_up()
                if l == 'KEY_PPAGE':
                    t_view.page_up()
                if l == 'KEY_NPAGE':
                    t_view.page_down()
                if l == 'KEY_DOWN':
                    t_view.scroll_down()
                if l == 'KEY_RIGHT':
                    t_view.scroll_right()
                if l == 'KEY_LEFT':
                    t_view.scroll_left()
                if l == "s":
                    utils.export(tab)
                if l in ('KEY_BACKSPACE', 'r', 'q'):
                    break
            r_view.refresh()
            show_tooltip(w_tips, tip_results)
        if k == 'q':
            break


def display_results(search):
    curses.wrapper(main, search)
