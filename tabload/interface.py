from curses import wrapper

def main(screen):
    screen.clear()

    for i in range(10):
        screen.addstr("Hello. I'm {}".format(i))

    screen.refresh()

wrapper(main)
