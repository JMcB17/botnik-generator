#!/usr/bin/env python


import argparse
from pathlib import Path

import youtube_dl as youtube_yl
from bs4 import BeautifulSoup


__version__ = '1.0.0'


def download(playlist_url: str, dest_folder: Path):
    pass


def merge_subtitles(sub_folder: Path, dest_file: Path):
    pass


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(name='--version', action='version', version=__version__)
    parser.parse_args()

    base_folder = Path('botnik_boards')
    # todo: change
    playlist_folder = base_folder
    dest_folder = playlist_folder / 'download'
    dest_folder.mkdir(parents=True, exist_ok=True)
    dest_file = base_folder / 'board.txt'

    playlist_url = input('Playlist url: ')
    print('Downloading...')
    download(playlist_url, dest_folder)

    print('Processing..')
    merge_subtitles(dest_folder, dest_file)
    print(
        'Done!\n'
        f'Created file {dest_file}\n'
        'Go to https://botnik.org/apps/writer/ and click the menu top left to create a new board from the file.'
    )


if __name__ == '__main__':
    main()
