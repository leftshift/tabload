import curses
import itertools

columns = "{title:{width['title']}}{artist:{width['artist']}}"

def _init(screen):
    curses.start_color()
    curses.use_default_colors()
    screen.clear()

def _get_page(search, items):
    return list(itertools.islice(search, 0, items))

def _display_page(window, search, results, starting_from, results_per_page):
    window.clear()
    results.extend(_get_page(search, height-2))
    resultset = results[starting_from:starting_from+results_per_page]

    z = zip(range(len(resultset)), resultset)

    for line, result in z:
        window.addstr(line, 0, result.title)

    window.refresh()


def main(screen, search):
    _init(screen)
    global height, width
    height, width = screen.getmaxyx()

    w_header = screen.derwin(2,width-1, 0,0)
    w_header.addstr("Test")
    w_header.hline(1,0, '-', width-1)
    w_header.refresh()

    w_results = screen.subwin(height-2, width, 2,0)

    results = []

    starting_from = 0
    results_per_page = w_results.getmaxyx()[0]

    while True:
        _display_page(w_results, search, results, starting_from, results_per_page)
        k = screen.getkey()
        if k == 'n':
            starting_from += results_per_page
        if k == 'p':
            starting_from -= results_per_page
        if k == 'q':
            break


def display_results(search):
    curses.wrapper(main, search)
