import re

from tabload.BaseSearch import BaseSearch
from tabload.BaseTab import BaseTab

instruments = set(['ukulele'])


class Search(BaseSearch):
    """docstring for UkuTabsSearch."""
    search_url = "https://ukutabs.com/page/{page}/?s={query}"

    def __init__(self, query):
        super(Search, self).__init__(query)

    def _get_number_of_pages(self):
        pagination = self.soup.find(class_='page-pagination')
        if not pagination:  # There is probably only one page
            return 1
        return max([int(t.text) for t in pagination.find_all()])

    def items(self, soup):
        table = soup.find(class_='latestlist3')
        if not table:
            raise StopIteration

        for li in table:
            type_ = li.find(class_='tabtype').string
            a = li.find_all('a')
            artist = a[0].string
            title = a[1].string
            url = a[1].get('href')
            yield Tab(url, title, artist, None, type_)


class Tab(BaseTab):
    """docstring for Tab."""
    service = "ukutabs"
    r_difficulty = re.compile("Difficulty level ([1-5]/5)")

    def __init__(self, url, title, artist, rating, type_):
        super(Tab, self).__init__(url, title, artist, rating, type_, "ukulele")

    def _parse_title(self, soup):
        td = soup.find('strong', text="Title").parent
        return td.next_sibling.find('span').text

    def _parse_artist(self, soup):
        td = soup.find('strong', text="Artist").parent
        return td.next_sibling.text.strip()

    def _parse_album(self, soup):
        td = soup.find('strong', text="Album").parent
        return td.next_sibling.text.strip()

    def _parse_difficulty(self, soup):
        a = soup.find(class_="kooltip")
        i = a.find("i")
        return self.r_difficulty.match(i.string).group(1)

    def _parse_capo(self, soup):
        b = soup.find(class_="boettonon")
        return b.get("value")

    def _parse_type(self, soup):
        # Type doesn't appear on actual page
        # If we got here from search results, just keep that
        # If we didn't, we simply don't know
        return self.type_

    def _parse_rating(self, soup):
        # No ratings
        return None

    def _parse_text(self, soup):
        pre = soup.select_one("div#cont pre")
        return pre.text

    def _parse_notes(self, soup):
        pre = soup.find("pre", class_="quotae-code", id="extranote")
        if pre:
            return pre.text
        else:
            return ""
