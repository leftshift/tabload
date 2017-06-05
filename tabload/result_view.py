import itertools
import curses

columns = "{title:{width['title']}}{artist:{width['artist']}}"


class ResultView:
    def __init__(self, window, search):
        height, width = window.getmaxyx()

        self.w_header = window.derwin(2,width-1, 0,0)
        self._display_header()
        self.w_results = window.derwin(height-2,width-1, 2,0)
        self.search = search

        self.results = []
        self._selected = 0
        self._screen_start = 0
        self._screen_end = 0

        self.items_per_page = self.w_results.getmaxyx()[0]

    @staticmethod
    def _generate_line(result):
        return result.title

    @staticmethod
    def _generate_header():
        pass

    def _display_header(self):
        width = self.w_header.getmaxyx()[1]

        self.w_header.addstr("Test")
        self.w_header.hline(1,0, '-', width)
        self.w_header.refresh()

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
            return False
        if starting_from < 0:  # a page before the first was requested
            return False

        self.w_results.clear()

        res_lines = zip(range(len(page)), page)

        for line, result in res_lines:
            self.w_results.addstr(line, 0, self._generate_line(result))

        self._screen_start = starting_from
        self._screen_end = starting_from + len(page)
        self._select(starting_from)

        self.w_results.refresh()
        return True

    def _select(self, item):
        self._selected = item

        curr_line = self._selected - self._screen_start
        self.w_results.addstr(curr_line, 0,
                              self._generate_line(self.results[self._selected]), curses.A_BOLD)
        self.w_results.refresh()

    def _select_and_clear(self, item):
        if item < self._screen_start or item >= self._screen_end:
            return None

        prev_selected = self._selected

        prev_line = prev_selected - self._screen_start
        self.w_results.addstr(prev_line, 0,
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
