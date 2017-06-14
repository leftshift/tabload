"""Base Class implementing a generator to access search results
from a website."""
import requests
from bs4 import BeautifulSoup

# TODO: Save instruments somewhere?


class BaseSearch(object):
    """Base Class for parsing search pages. Acts as a Generator.

    To adapt to a new page, change the search_url to reflect the sites'
    url scheme for query and page.

    Implement _get_number_of_pages() if the number of pages can be parsed
    from the first result page, otherwise adjust pages().

    Implement items() as a generator that yields search results as
    Tab() objects"""

    search_url = "https://test.org/?s={query}&p={page}"

    def __init__(self, query):
        self.query = query
        html = requests.get(self.search_url.format(query=query, page=1)).text
        self.soup = BeautifulSoup(html, 'lxml')
        self.iter = self.results()

    def __iter__(self):
        """Act as an iterator/generator"""
        return self

    def _get_number_of_pages(self):
        """Parses the number of search result pages from the first page via self.soup.

        Returns
        -------
        int
            Number of pages
        """
        raise NotImplementedError

    def results(self):
        """The main generator function. Yields `Tab`s for the given query."""
        import pudb; pudb.set_trace()
        for page in self.pages(self.soup):
            self.soup = page
            for item in self.items(self.soup):
                yield item

    def pages(self, soup):
        """The generator for accessing all the search result pages.
        Yields `BeautifulSoup`s for all the pages."""
        n = self._get_number_of_pages()
        yield soup  # yield the already loaded page
        for i in range(2, self._get_number_of_pages()+1):
            html = requests.get(self.search_url.format(query=self. query, page=i)).text
            soup = BeautifulSoup(html, 'html.parser')
            yield soup

    def items(self, soup):
        """The generator for accessing items in a result page.
        Yields `Tab` objects."""
        raise NotImplementedError

    def __next__(self):
        """Wrapper to make `BaseSearch` itself act as a generator.
        Returns the next iteration from an instance of the `results`
        generator."""
        return self.iter.__next__()

    def __repr__(self):
        return "<Search(query={self.query})>".format(self=self)
