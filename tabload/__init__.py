import argparse


def main():
    parser = argparse.ArgumentParser(description="Downloads Tabs or Chords from various sites and exports them to different formats.")

    parser.add_argument("Title or URL",
                        help="Search String to search for")
    parser.add_argument("-f", "--format",
                        help="Output format",
                        default="txt")
    parser.add_argument("-i", "--instrument",
                        help="The Instrument for wich tabs should be searched")
    parser.add_argument("-s", "--service",
                        help="Name(s) of the services to search",
                        nargs='+')
    print(parser.parse_args())

if __name__ == '__main__':
    main()
