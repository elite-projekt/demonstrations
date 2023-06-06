#!/usr/bin/env python3

import pathlib
import sys

from argparse import ArgumentParser, RawTextHelpFormatter

EXTENSIONS = ["png", "jpg", "jpeg", "gif", "svg",
              "wav", "flac", "opus", "ogg", "mp3",
              "mkv", "mp4", "avi"]


def main():
    parser = ArgumentParser(formatter_class=RawTextHelpFormatter)
    parser.add_argument("-f", "--folder", dest="folder",
                        help="Folder to scan", type=str, required=True)
    args = parser.parse_args()

    folder = pathlib.Path(args.folder).absolute()

    all_files = []
    for file_type in EXTENSIONS:
        for f in folder.glob(f"**/*.{file_type}"):
            all_files.append(f)

    files_without_license = []
    for media_file in all_files:
        if (pathlib.Path(media_file.parent) / ".ignorelicense").exists():
            continue
        license_path = pathlib.Path(media_file.parent / "LICENSE")
        if license_path.exists():
            with open(media_file.parent / "LICENSE", "r") as license_file:
                text = license_file.read()
                if media_file.name not in text:
                    files_without_license.append(media_file)
        else:
            files_without_license.append(media_file)

    if len(files_without_license) > 0:
        print("We found media files without a license!")
        for f in files_without_license:
            print(f)
        sys.exit(1)


if __name__ == "__main__":
    main()
