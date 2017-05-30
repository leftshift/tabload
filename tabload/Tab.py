import requests
from bs4 import BeautifulSoup


class Tab():
    """docstring for Tab."""
    def __init__(self, url, title, artist, rating, type_):
        self.url = url
        self.title = title
        self.artist = artist
        self.rating = rating
        self.type = type_

    def load(self):
        _load_html()
        _parse()

    def _load_html(self):
        self.html = requests.get(self.url)

    def _parse(self):
        soup = BeautifulSoup(self.html, 'html.parser')
        _parse_title(soup)
        _parse_artist(soup)
        _parse_album(soup)
        _parse_difficulty(soup)
        _parse_capo(soup)
        _parse_type(soup)
        _parse_rating(soup)
        _parse_text(soup)

    def _parse_title(self, soup):
        raise NotImplementedError

    def _parse_artist(self, soup):
        raise NotImplementedError

    def _parse_album(self, soup):
        raise NotImplementedError

    def _parse_difficulty(self, soup):
        raise NotImplementedError

    def _parse_capo(self, soup):
        raise NotImplementedError

        def _parse_type(self, soup):
            raise NotImplementedError

    def _parse_text(self, soup):
        raise NotImplementedError

    def _parse_rating(self, soup):
        raise NotImplementedError
