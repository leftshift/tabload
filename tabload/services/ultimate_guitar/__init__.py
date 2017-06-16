import re

from tabload.BaseSearch import BaseSearch
from tabload.BaseTab import BaseTab

instruments = set(['ukulele', 'guitar', 'bass', 'drums'])


class Search(BaseSearch):
    """docstring for UltimateGuitarSearch."""
    search_url = "https://www.ultimate-guitar.com/search.php%7Csearch.php3?search_type=title&order=&value={query}&page={page}"

    def __init__(self, query):
        super(Search, self).__init__(query)

    def _get_number_of_pages(self):
        pagination = self.soup.find(class_='pagination')
        if not pagination:  # There is probably only one page
            return 1
        return max([int(t.text) for t in pagination.find_all('li') if not (t.text == "« Prev" or t.text == "Next »")])

    def items(self, soup):
        table = soup.find(class_="tresults")
        if not table:
            raise StopIteration

        trs = table.find_all("tr")

        for tr in trs[1:]:  # Skip first, that's the header
            cols = tr.find_all("td")

            if cols[0].get("id") == "npd77":
                del cols[0]
            if cols[0].text.strip():  # Artist column isn't empty
                artist = cols[0].text.strip()
            url = cols[1].find("a").get('href')
            title = cols[1].find("a").text.strip()
            rating = None
            typ = cols[3].text.strip()

            if "pro" not in typ and typ not in ("official", "power", "video"):
                yield Tab(url, title, artist, rating, typ)


class Tab(BaseTab):
    """docstring for Tab."""
    service = "ultimate_guitar"
    r_difficulty = re.compile("Difficulty level ([1-5]/5)")

    def __init__(self, url, title, artist, rating, type_):
        if type_ not in ("chords", "tab"):
            instrument = type_
        else:
            instrument = ""
        super(Tab, self).__init__(url, title, artist, rating, type_, instrument)

    def _parse_title(self, soup):
        title_div = soup.find(class_="t_title")
        title = title_div.find("h1").text.strip()

        version_div = title_div.find(class_="t_version")
        if version_div:
            title += " " + version_div.text.strip()
        return title

    def _parse_artist(self, soup):
        title_div = soup.find(class_="t_title")
        author_div = title_div.find(class_="t_autor")
        return author_div.find("a").text

    def _parse_album(self, soup):
        return None

    def _parse_difficulty(self, soup):
        return None  # No difficulty

    def _parse_capo(self, soup):
        return ""  # TODO:

    def _parse_type(self, soup):
        # Type doesn't appear on actual page
        # If we got here from search results, just keep that
        # If we didn't, we simply don't know
        return self.type_

    def _parse_rating(self, soup):
        # TODO:
        return None

    def _parse_text(self, soup):
        pre = soup.find(class_="js-tab-content")
        return pre.text.replace("\r\n", "\n")

    def _parse_notes(self, soup):
        return soup.find(class_="b-tab-meta").text
