import curses
import itertools


def _init(screen):
    curses.start_color()
    curses.use_default_colors()
    screen.clear()


def _get_page(search, items):
    return list(itertools.islice(search, 0, items))


def main(screen, search):
    _init(screen)
    height, width = screen.getmaxyx()

    results = []
    results.append(_get_page(search, 5))

    z = zip(range(len(results[0])), results[0])

    import pudb; pudb.set_trace()

    for line, result in zip(range(len(results[0])), results[0]):
        screen.addstr(line, 0, result.title)

    screen.refresh()
    k = screen.getkey()


def display_results(search):
    curses.wrapper(main, search)
