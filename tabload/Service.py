import requests

class Service():
    """docstring for Service."""
    search_url = "https://test.org/?s={query}"
    instruments = []

    def __init__(self):
        pass

    @classmethod
    def search(cls, query):
        print(cls.search_url)
        results = []
        html = requests.get(cls.search_url.format(query=query)).text

        for page in range(cls._get_number_of_pages()):
            html = requests.get(cls.search_url.format(query=query)).text
            results.append(cls._parse_search(html, query))

    @classmethod
    def _get_number_of_pages(cls):
        pass

    # TODO: _get_number_of_pages()
    # TODO: results_page_url {page}
    # TODO: Probably better: use Search class with state and generator or sth like that

    @classmethod
    def _parse_search(cls, html, query):
        """Returns array of Tab objects found
        """
        raise NotImplementedError
