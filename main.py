#!/usr/bin/env python


import argparse
from pathlib import Path

import youtube_dl as youtube_yl
from bs4 import BeautifulSoup


__version__ = '1.0.0'


def download(playlist_url: str, dest_folder: Path):
    ydl_opts = {
        # 'playlistend': 3,
        'writesubtitles': True,
        'writeautomaticsub': True,
        'subtitlesformat': 'vtt',
        'outtmpl': f'{dest_folder}\\{youtube_yl.DEFAULT_OUTTMPL}',
    }

    with youtube_yl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([playlist_url])


def merge_subtitle_file(sub_file_path: Path) -> str:
    with open(sub_file_path) as sub_file:
        subs = BeautifulSoup(sub_file, 'html.parser')

    subs_strings = []
    for sub in subs.find_all('p'):
        subs_strings.append(sub.string)

    return '\n'.join(subs_strings)


def merge_subtitles_in_folder(sub_folder: Path, dest_file_path: Path):
    with open(dest_file_path, 'w') as dest_file:
        for sub_file in sub_folder.iterdir():
            dest_file.write(merge_subtitle_file(sub_file))


def main():
    parser = argparse.ArgumentParser(
        description='Create a new Botnik AI predictive keyboard from a youtube playlist by downloading its subtitles.'
    )
    parser.add_argument('--version', action='version', version=__version__)
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
    merge_subtitles_in_folder(dest_folder, dest_file)
    print(
        'Done!\n'
        f'Created file {dest_file}\n'
        'Go to https://botnik.org/apps/writer/ and click the menu top left to create a new board from the file.'
    )


if __name__ == '__main__':
    main()
