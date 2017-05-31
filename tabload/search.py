import tabload.services
# all services: tabload.services.__all__

# TODO: Move to config/Make user configurable
default_services = tabload.services.__all__
default_instruments = ['chords']


def combined_results(results):
    while True:
        for service, search in results.items():
            if not any([s for s in results.values()]):  # All have been died
                raise StopIteration

            if not search:  # All results have been consumed, skip this search
                continue

            try:
                yield search.__next__()
            except StopIteration:
                # All results for this service have been consumed,
                # we can delete the search
                results[service] = None
                continue


def search(query, instruments=default_instruments,
           services=default_services, items=10):
    results = {}

    service_mods = [getattr(tabload.services, s) for s in services]

    for service, module in zip(services, service_mods):
        results[service] = module.Search(query)

    combined = combined_results(results)

    while True:
        page = []
        while len(page) < items:
            page.append(combined.__next__())
        print(page)
        yield page
