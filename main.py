#!/usr/bin/env python

import argparse
from pathlib import Path

import youtube_dl as youtube_yl
from bs4 import BeautifulSoup


__version__ = '1.1.0'
BASE_FOLDER_NAME = 'botnik-boards'


# todo: speed up somehow with threading?
def download(playlist_url: str, dest_folder: Path, lang: str = None):
    ydl_opts = {
        # 'playlistend': 3,
        'skip_download': True,
        'writesubtitles': True,
        'writeautomaticsub': True,
        'subtitlesformat': 'ttml',
        'outtmpl': f'{dest_folder}\\{youtube_yl.DEFAULT_OUTTMPL}',
        'ignoreerrors': True,
    }
    if lang:
        ydl_opts['subtitleslangs'] = [lang]

    with youtube_yl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([playlist_url])


def merge_subtitle_file(sub_file_path: Path) -> str:
    with open(sub_file_path, encoding='utf-8') as sub_file:
        subs = BeautifulSoup(sub_file, 'html.parser')

    subs_strings = []
    for sub in subs.find_all('p'):
        subs_strings.append('\n'.join(sub.strings))
    subs_strings.append('\n')

    return '\n'.join(subs_strings)


def merge_subtitles_in_folder(sub_folder: Path, dest_file_path: Path):
    with open(dest_file_path, 'w', encoding='utf-8') as dest_file:
        for sub_file in sub_folder.iterdir():
            dest_file.write(merge_subtitle_file(sub_file))


def shorten_file(source_file_path: Path, dest_file_path: Path, limit: int = 10**6):
    with open(dest_file_path, 'w', encoding='utf-8') as dest_file:
        with open(source_file_path, encoding='utf-8') as source_file:
            dest_file.writelines(source_file.readlines(limit))


def main():
    parser = argparse.ArgumentParser(
        description='Create a new Botnik AI predictive keyboard from a youtube playlist by downloading its subtitles.'
    )
    parser.add_argument('--version', action='version', version=__version__)
    parser.add_argument('playlist_url', nargs='?')
    parser.add_argument('-l', '--lang', help='the subtitle language to download as a two-letter code e.g. en (english)')
    parser.add_argument('-f', '--folder', help='name of the folder to download to, will be created if not exists')
    args = parser.parse_args()

    if args.playlist_url:
        playlist_url = args.playlist_url
    else:
        playlist_url = input('Playlist url: ')
    if args.folder:
        playlist_folder_name = args.folder
    else:
        # todo: check this with regex?
        playlist_folder_name = input('Output folder name: ')

    current_folder = Path().resolve()
    if current_folder.name == BASE_FOLDER_NAME:
        base_folder = current_folder
    else:
        base_folder = Path(BASE_FOLDER_NAME)
    playlist_folder = base_folder / playlist_folder_name
    dest_folder = playlist_folder / 'download'
    dest_folder.mkdir(parents=True, exist_ok=True)
    dest_file = base_folder / 'board.txt'
    dest_file_1m = dest_file.with_stem(dest_file.stem + '-500kB')

    print('Downloading...')
    download(playlist_url, dest_folder, args.lang)

    print('Processing..')
    merge_subtitles_in_folder(dest_folder, dest_file)
    shorten_file(dest_file, dest_file_1m, (10**6)//2)
    print(
        'Done!\n'
        f'Created file {dest_file}\n'
        'Go to https://botnik.org/apps/writer/ and click the menu top left to create a new board from the file.'
    )


if __name__ == '__main__':
    main()
