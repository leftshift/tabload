from tabload.Search import Search as BaseSearch
from tabload.Tab import Tab as BaseTab


class Search(BaseSearch):
    """docstring for UkuTabsSearch."""
    search_url = "https://ukutabs.com/page/{page}/?s={query}"

    def __init__(self, query):
        super(Search, self).__init__(query)

    def _get_number_of_pages(self):
        pagination = self.soup.find(class_='page-pagination')
        return max([int(t.text) for t in pagination.find_all()])

    def items(self):
        table = self.soup.find(class_='latestlist3')
        for li in table:
            typ = li.find(class_='tabtype').string
            a = li.find_all('a')
            artist = a[0].string
            title = a[1].string
            url = a[1].get('href')
            yield Tab(url, title, artist, None, typ)


class Tab(BaseTab):
    """docstring for Tab."""
    def __init__(self, url, title, artist, rating, type_):
        super(Tab, self).__init__(url, title, artist, rating, type_)

    def _parse_title(self, soup):
        td = soup.find('strong', text="Title").parent
        return td.next_sibling.find('span').text
