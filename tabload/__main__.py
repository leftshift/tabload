import argparse
import tabload.search
import tabload.interface
from tabload import g


def main():
    parser = argparse.ArgumentParser(description="Downloads Tabs or Chords from \
    various sites and exports them to different formats.")

    parser.add_argument("String",
                        help="String to search for")
    parser.add_argument("-f", "--format",
                        help="Output format",
                        default="text")
    parser.add_argument("-i", "--instruments",
                        help="The Instrument for wich tabs should be searched",
                        default=g.instruments,
                        nargs='+')
    parser.add_argument("-s", "--services",
                        help="Name(s) of the services to search",
                        default=g.services,
                        nargs='+')
    parser.add_argument("-c", "--chords",
                        help="Show chord diagrams",
                        action="store_true")
    args = parser.parse_args()

    if hasattr(args, 'format'):
        g.export_format = args.format
    if hasattr(args, 'instruments'):
        g.instruments = args.instruments
    if hasattr(args, 'services'):
        g.services = args.services
    if args.chords:
        try:
            import chordata.utils
            instrument_name = g.ch_mapping.get(g.instruments[0])
            g.ch_instrument = chordata.utils.get_instrument(instrument_name)
            g.ch_diff_dict = chordata.utils.build_diff_dict(g.ch_instrument[1])
            g.chord_diagrams = True
        except Exception as e:
            print("Chord diagrams failed:{}".format(e))

    print(args)

    search = tabload.search.search(args.String, g.instruments, g.services)

    tabload.interface.display_results(search)


if __name__ == '__main__':
    main()
