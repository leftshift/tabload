from tabload import Service


class UkuTabs(Service):
    """docstring for UkuTabs."""
    search_url = "https://ukutabs.com/?s={query}"
    instruments = ["ukulele"]

    def __init__(self):
        super(UkuTabs, self).__init__()
        pass

    def _parse_search(self, query):
        print(query)
