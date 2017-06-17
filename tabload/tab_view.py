import curses
import tabload.formats.text

class TabView:
    """docstring for TabView."""
    def __init__(self, window, tab):
        self.window = window
        self.window.clear()
        self.window.refresh()
        self.tab = tab
        if not self.tab.loaded:
            self.tab.load()

        clip_box = []
        # get the lowermost coordinates of the window
        endxy = [i + j - 1 for i, j in zip(window.getbegyx(), window.getmaxyx())]
        clip_box.extend(window.getbegyx())
        clip_box.extend(endxy)

        self.clip_box = clip_box
        self._load_text()

        self.posx = 0
        self.posy = 0

    def _load_text(self):
        text = tabload.formats.text.generate(self.tab)
        self.height = len(text.split('\n'))
        self.width = max([len(line) for line in text.split('\n')])

        self.pad = curses.newpad(self.height, self.width)
        self.pad.insstr(text)

    def show(self):
        self.pad.refresh(self.posy, self.posx, *self.clip_box)

    def transpose_up(self):
        self.tab.transpose(1)
        self._load_text()
        self.show()

    def transpose_down(self):
        self.tab.transpose(-1)
        self._load_text()
        self.show()

    def scroll_up(self, amount=1):
        self.posy = max(0, self.posy - amount)
        self.show()

    def scroll_down(self, amount=1):
        if self.posy + amount + self.window.getmaxyx()[0] < self.height:
            self.posy = self.posy + amount
        else:
            # Scrolling of amount is not possible, so scroll to a position where everything up to the last line is visible
            self.posy = self.height - self.window.getmaxyx()[0]
        self.show()

    def scroll_left(self, amount=1):
        self.posx = max(0, self.posx - amount)
        self.show()

    def scroll_right(self, amount=1):
        if self.posx + amount + self.window.getmaxyx()[1] < self.width:
            self.posx = self.posx + amount
        else:
            self.posx = self.width - self.window.getmaxyx()[1]
        self.show()

    def page_up(self):
        self.scroll_up(self.window.getmaxyx()[0])

    def page_down(self):
        self.scroll_down(self.window.getmaxyx()[0])
