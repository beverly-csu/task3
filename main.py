from tinytag import TinyTag
import argparse
import os


def cut_and_paste(dst_path, true_name, track_name, full_path):
    try:
        os.mkdir(dst_path)
        dst_path = os.path.join(dst_path, true_name)
        if os.path.exists(dst_path):
            print('Файл <', track_name, "> уже существует в конечной директории.")
        else:
            os.rename(full_path, dst_path)
            print(full_path, "->", dst_path)
    except OSError:
        dst_path = os.path.join(dst_path, true_name)
        if os.path.exists(dst_path):
            print('Файл <', track_name, '> уже существует в конечной директории.')
        else:
            os.rename(full_path, dst_path)
            print(full_path, '->', dst_path)


def track_sorter(track_list, src_dir='', dst_dir=''):
    for track_name in track_list:
        full_path = os.path.join(src_dir, track_name)
        track = TinyTag.get(full_path)
        if track.artist and track.album:
            true_name = str(track.title) + ' - ' + str(track.artist) + ' - ' + str(track.album) + '.mp3'
            dst_path = os.path.join(dst_dir, str(track.artist))
            if track.title is None:
                true_name = track_name
            try:
                os.mkdir(dst_path)
                dst_path = os.path.join(dst_path, str(track.album))
                cut_and_paste(dst_path, true_name, track_name, full_path)
            except OSError:
                dst_path = os.path.join(dst_path, track.album)
                cut_and_paste(dst_path, true_name, track_name, full_path)
        else:
            print('У файла <', track_name, '> отсутствуют ID3 теги.')


def music_list(src_dir):
    track_list = []
    ext = '.mp3'
    for file in os.listdir(src_dir):
        if file.endswith(ext):
            track_list.append(file)
    return track_list


def main():
    desc = 'Программа для группировки музыки по ID3 тегам. По умолчанию используется папка где находится скрипт'
    parser = argparse.ArgumentParser(description=desc, add_help=False)
    parser._optionals.title = 'Возможные аргументы'
    parser.add_argument('-s', default="", help='Путь до исходной папки', required=False, dest='src')
    parser.add_argument('-d', default="", help='Путь до папки назначения', required=False, dest='dst')
    parser.add_argument('-h', '--help', action='help', default=argparse.SUPPRESS,
                        help='Справка о консольном приложении')
    args = parser.parse_args()
    if args.src != '':
        src_dir = os.path.abspath(args.src)
        print('Исходная папка:', os.path.abspath(args.src))
    else:
        src_dir = os.getcwd()
    if args.dst != '':
        dst_dir = os.path.abspath(args.dst)
        print('Папка назначения:', os.path.abspath(args.dst))
    else:
        dst_dir = os.getcwd()
    track_list = music_list(src_dir)
    track_sorter(track_list, src_dir, dst_dir)


if __name__ == '__main__':
    main()
