import itertools
import curses

class ResultView:
    def __init__(self, window, search):
        self.window = window
        self.search = search

        self.results = []
        self._selected = 0
        self._screen_start = 0
        self._screen_end = 0

        self.items_per_page = window.getmaxyx()[0]

    @staticmethod
    def _generate_line(result):
        return result.title

    def display_page(self, starting_from):
        if starting_from + self.items_per_page > len(self.results):
            # The number of results to be shown is larger than the number of results loaded
            self.results.extend(
                list(itertools.islice(
                    self.search, 0, self.items_per_page)
                )
            )

        page = self.results[starting_from:starting_from + self.items_per_page]

        if not page:  # there are no more results
            return None
        if starting_from < 0:  # a page before the first was requested
            return None

        self.window.clear()

        res_lines = zip(range(len(page)), page)

        for line, result in res_lines:
            self.window.addstr(line, 0, self._generate_line(result))

        self._screen_start = starting_from
        self._screen_end = starting_from + len(page)
        self._select(starting_from)

        self.window.refresh()

    def _select(self, item):
        self._selected = item

        curr_line = self._selected - self._screen_start
        self.window.addstr(curr_line, 0,
                           self._generate_line(self.results[self._selected]), curses.A_BOLD)
        self.window.refresh()

    def _select_and_clear(self, item):
        if item < self._screen_start or item >= self._screen_end:
            return None

        prev_selected = self._selected

        prev_line = prev_selected - self._screen_start
        self.window.addstr(prev_line, 0,
                           self._generate_line(self.results[prev_selected]))

        self._select(item)

    def next_page(self):
        new_start = self._screen_start + self.items_per_page
        self.display_page(new_start)

    def prev_page(self):
        new_start = self._screen_start - self.items_per_page
        self.display_page(new_start)

    def next_item(self):
        self._select_and_clear(self._selected + 1)

    def prev_item(self):
        self._select_and_clear(self._selected - 1)

    def get_curr_item(self):
        return self.results[self._selected]
