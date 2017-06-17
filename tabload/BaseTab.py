"""Base Class for tab or chord sheets"""

import requests
import re
from bs4 import BeautifulSoup

from tabload import g
from tabload import utils


class BaseTab():
    """Acts both as a representation of a search result and a
    fully downloaded Tab.

    To adapt to a service, you'll probably only have to implement
    all the _parse_foo()-functions and set the `service` string."""

    service = None

    def __init__(self, url, title, artist, rating, type_, instrument):
        self.url = url
        self.title = title
        self.artist = artist
        self.rating = rating
        self.type_ = type_
        self.instrument = instrument
        self.loaded = False

    def load(self):
        """Call this to download the html for this Tab and parse it."""
        self._load_html()
        self._parse()
        self.loaded = True

    def transpose(self, semitones):
        assert self.loaded
        # TODO: Maybe keep around original text?
        self.text = g.r_chord.sub(utils.transposer(semitones), self.text)

    def get_chords(self):
        assert self.loaded
        return set(g.r_chord.findall(self.text))

    def _load_html(self):
        self.html = requests.get(self.url).text

    def _parse(self):
        """Creates a soup from the downloaded html, passes it to all the
        parse functions and sets the attributes accordingly."""
        soup = BeautifulSoup(self.html, 'lxml')
        self.title = self._parse_title(soup)
        self.artist = self._parse_artist(soup)
        self.album = self._parse_album(soup)
        self.difficulty = self._parse_difficulty(soup)
        self.capo = self._parse_capo(soup)
        self.type_ = self._parse_type(soup)
        self.rating = self._parse_rating(soup)
        self.text = self._parse_text(soup)
        self.notes = self._parse_notes(soup)

    def _parse_title(self, soup):
        """Returns the title of this tab, given the
        BeautifulSoup representation of the page."""
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
