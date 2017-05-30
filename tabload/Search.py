import requests
from bs4 import BeautifulSoup

# TODO: Save instruments somewhere?


class Search(object):
    """docstring for Search."""
    search_url = "https://test.org/?s={query}&p={page}"

    def __init__(self, query):
        self.query = query
        html = requests.get(self.search_url.format(query=query, page=1)).text
        self.soup = BeautifulSoup(html, 'html.parser')
        self.iter = self.results()

    def __iter__(self):
        return self

    def _get_number_of_pages(self):
        raise NotImplementedError

    def results(self):
        for page in self.pages():
            for item in self.items():
                yield item

    def pages(self):
        n = self._get_number_of_pages()
        yield self.soup  # yield the already loaded page
        for i in range(2, self._get_number_of_pages()+1):
            html = requests.get(self.search_url.format(query=self. query, page=i)).text
            self.soup = BeautifulSoup(html, 'html.parser')
            yield

    def items(self):
        # yield Tab()
        raise NotImplementedError

    def __next__(self):
        return self.iter.__next__()
