import argparse
import tabload.search
import tabload.interface
from tabload import g


def main():
    parser = argparse.ArgumentParser(description="Downloads Tabs or Chords from various sites and exports them to different formats.")

    parser.add_argument("String",
                        help="String to search for")
    parser.add_argument("-f", "--format",
                        help="Output format",
                        default="text")
    parser.add_argument("-i", "--instruments",
                        help="The Instrument for wich tabs should be searched",
                        nargs='+')
    parser.add_argument("-s", "--services",
                        help="Name(s) of the services to search",
                        nargs='+')
    args = parser.parse_args()

    if hasattr(args, 'format'):
        g.export_format = args.format
    if hasattr(args, 'instruments'):
        g.instruments = args.instruments
    if hasattr(args, 'services'):
        g.services = args.services

    print(args)

    search = tabload.search.search(args.String)

    tabload.interface.display_results(search)



if __name__ == '__main__':
    main()
