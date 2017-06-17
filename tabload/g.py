"""Manages some global settings and variables"""
import re

r_chord = re.compile("\s([ABCDEFG](?:#{1,2}|b{1,2})?[1-9]?(?:M|maj|major|m|min|minor|dim|sus|dom|aug|\+|-|add)?[1-9]?)\s")

export_format = "text"
instruments = ['guitar', 'ukulele', 'bass']
services = ["ukutabs", "ultimate_guitar"]

name_scheme = "{tab.artist} – {tab.title}.{suffix}"
out_dir = "./out"
