import argparse
from os.path import join

from .downloader import download_course, download_nanodegree
from .request import *
from .utils.renderer import Renderer

parser = argparse.ArgumentParser(description='Download udacity course')

subparsers = parser.add_subparsers()

course_parser = subparsers.add_parser('course')
course_parser.set_defaults(function=download_course)
course_parser.add_argument('course_id', type=str, help='Course ID', nargs='+')

nanodegree_parser = subparsers.add_parser('nanodegree')
nanodegree_parser.set_defaults(function=download_nanodegree)
nanodegree_parser.add_argument('nanodegree_id', type=str, help='Nanodegree ID')

for _parser in (course_parser, nanodegree_parser):
    _parser.add_argument('--outdir', '-o', required=True, type=str, help='Output directory')

    _parser.add_argument("--username", "-u", required=True, type=str, help="Udacity account username/email")
    _parser.add_argument("--password", "-p", required=True, type=str, help="Udacity account password")
    
    _parser.add_argument('--download-resources', '-d', action='store_true', help="Download resources for each lesson")
    _parser.add_argument('--flat', '-l', action='store_true', help="Don't create a directory with the name of the course")


def main():
    args = parser.parse_args()
    args.function(args)


if __name__ == '__main__':
    main()
