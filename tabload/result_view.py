import itertools
import curses


class ResultView:
    columns = ['title', 'artist', 'service']

    def __init__(self, window, search):
        height, width = window.getmaxyx()

        self.w_header = window.derwin(2,width-1, 0,0)

        self._max_width = self.w_header.getmaxyx()[1] // len(self.columns)
        self.generate_format_string()
        self._display_header()
        self.w_results = window.derwin(height-2,width-1, 2,0)
        self.search = search

        self.results = []
        self._selected = 0
        self._screen_start = 0
        self._screen_end = 0

        self.items_per_page = self.w_results.getmaxyx()[0]

    def generate_format_string(self):
        width = {}
        # for column in self.colums:
        #     longest = max([len(getattr(column, r)) for r in self.results])
        #     width = min(longest, max_width)

        format_string = []

        for column in self.columns:
            line = "{{:<{width}}}".format(width=self._max_width)
            format_string.append(line)

        self.format_string = ''.join(format_string)


    def _generate_line(self, result):
        t = [getattr(result, a)[:self._max_width-1] for a in self.columns]
        return self.format_string.format(*t)

    def _generate_header(self):
        t = [c[:self._max_width] for c in self.columns]
        return self.format_string.format(*t)

    def _display_header(self):
        width = self.w_header.getmaxyx()[1]

        self.w_header.insstr(self._generate_header())
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

        for line, result in enumerate(page):
            self.w_results.insstr(line, 0, self._generate_line(result))

        self._screen_start = starting_from
        self._screen_end = starting_from + len(page)
        self._select(starting_from)

        self.w_results.refresh()
        return True

    def _select(self, item):
        self._selected = item

        curr_line = self._selected - self._screen_start
        self.w_results.insstr(curr_line, 0,
                              self._generate_line(self.results[self._selected]), curses.A_BOLD)
        self.w_results.refresh()

    def _select_and_clear(self, item):
        if item < self._screen_start or item >= self._screen_end:
            return None

        prev_selected = self._selected

        prev_line = prev_selected - self._screen_start
        self.w_results.insstr(prev_line, 0,
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

    def refresh(self):
        selection = self._selected
        self.w_header.clear()
        self.w_results.clear()

        self._display_header()
        self.display_page(self._screen_start)

        self._select_and_clear(selection)
