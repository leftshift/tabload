import re

from tabload.BaseSearch import BaseSearch
from tabload.BaseTab import BaseTab


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

            if "pro" not in typ and typ != "official":
                yield Tab(url, title, artist, rating, typ)


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
