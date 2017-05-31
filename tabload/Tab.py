import requests
from bs4 import BeautifulSoup


class Tab():
    """docstring for Tab."""
    def __init__(self, url, title, artist, rating, type_, instrument):
        self.url = url
        self.title = title
        self.artist = artist
        self.rating = rating
        self.type = type_
        self.instrument = instrument

    def load(self):
        self._load_html()
        self._parse()

    def _load_html(self):
        self.html = requests.get(self.url).text

    def _parse(self):
        soup = BeautifulSoup(self.html, 'lxml')
        self.title = self._parse_title(soup)
        self.artist = self._parse_artist(soup)
        self.album = self._parse_album(soup)
        self.difficulty = self._parse_difficulty(soup)
        self.capo = self._parse_capo(soup)
        self.type = self._parse_type(soup)
        self.rating = self._parse_rating(soup)
        self.text = self._parse_text(soup)
        self.notes = self._parse_notes(soup)

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

    def _parse_rating(self, soup):
        raise NotImplementedError

    def _parse_text(self, soup):
        raise NotImplementedError

    def _parse_notes(self, soup):
        raise NotImplementedError

    def __repr__(self):
        return "<Tab(url={self.url}, title={self.title}, artist={self.artist})>".format(self=self)
