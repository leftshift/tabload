import curses
import tabload.formats.text

class TabView:
    """docstring for TabView."""
    def __init__(self, window, tab):
        self.window = window
        self.window.clear()
        self.window.refresh()
        self.tab = tab
        if not tab.loaded:
            self.tab.load()

        clip_box = []
        # get the lowermost coordinates of the window
        endxy = [i + j - 1 for i, j in zip(window.getbegyx(), window.getmaxyx())]
        clip_box.extend(window.getbegyx())
        clip_box.extend(endxy)

        self.clip_box = clip_box
        text = tabload.formats.text.generate(self.tab)
        self.height = len(text.split('\n'))
        self.width = max([len(line) for line in text.split('\n')])

        self.pad = curses.newpad(self.height, self.width)
        self.pad.insstr(text)

        self.posx = 0
        self.posy = 0

    def show(self):
        self.pad.refresh(self.posy, self.posx, *self.clip_box)

    def scroll_up(self):
        self.posy = max(0, self.posy-1)
        self.show()

    def scroll_down(self):
        if self.posy + 1 + self.window.getmaxyx()[0] < self.height:
            self.posy = self.posy+1
            self.show()
