import tabload.services


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


def search(query, instruments, services):
    results = {}

    service_mods = []

    for service in services:
        module = getattr(tabload.services, service)
        if module.instruments.intersection(instruments):
            service_mods.append(module)

    for service, module in zip(services, service_mods):
        results[service] = module.Search(query)

    combined = combined_results(results)
    while True:
        yield combined.__next__()
