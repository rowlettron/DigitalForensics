#!/usr/bin/env python3

import argparse
import hashlib
import os
import shutil
import sys
import time

HASH_FILE_CHUNK_SIZE = 8192
HASH_ZERO_FILE = "0" * 40


class Console:
    TERMINAL_CONNECTED = sys.stdout.isatty()
    TERMINAL_SIZE_CACHE_SECONDS = 2
    CURSOR_START_LINE_CLEAR_RIGHT = "{0}{1}".format("\r", "\x1b[K")

    DOT_GAP_MIN_LENGTH = 3
    TEXT_SPLIT_MIN_LENGTH = 5

    class TERM_COLOR:
        RESET = "\x1b[0m"
        YELLOW = "\x1b[33m"

    progress_enabled = False

    _progress_active = False
    _last_term_size = (0, 0, 0)

    def _terminal_size(self) -> tuple[int, int]:
        now_timestamp = int(time.time())

        if now_timestamp >= (
            Console._last_term_size[0] + Console.TERMINAL_SIZE_CACHE_SECONDS
        ):
            # (re-)fetch terminal dimensions
            size = shutil.get_terminal_size()
            Console._last_term_size = (now_timestamp,) + size
            return size

        # return previously stored cols and rows
        return (Console._last_term_size[1], Console._last_term_size[2])

    def _text_truncated(self, text: str, max_length: int) -> str:
        if len(text) < max_length:
            # no need for truncation
            return text

        # determine dot gap length - 5% of max length, plus two space characters
        dot_gap = int(max_length * 0.05) + 2
        if dot_gap < Console.DOT_GAP_MIN_LENGTH:
            dot_gap = Console.DOT_GAP_MIN_LENGTH

        # calculate split size - if too small just truncate and bail
        split_size = int((max_length - dot_gap) / 2)
        if split_size < Console.TEXT_SPLIT_MIN_LENGTH:
            return text[:max_length].strip()

        # return [HEAD_CHUNK ... TAIL_CHUNK]
        return "{0} {1} {2}".format(
            text[:split_size].strip(),
            +((max_length - (split_size * 2)) - 2) * ".",
            text[0 - split_size :].strip(),
        )

    def _write_flush(self, text: str) -> None:
        sys.stdout.write(text)
        sys.stdout.flush()

    def _progress_end(self) -> None:
        if not Console._progress_active:
            return

        # clean up progress line from terminal, reset foreground color
        Console._progress_active = False
        self._write_flush(
            Console.CURSOR_START_LINE_CLEAR_RIGHT + Console.TERM_COLOR.RESET
        )

    def exit_error(self, message: str) -> None:
        self._progress_end()
        print(f"Error: {message}", file=sys.stderr)
        sys.exit(1)

    def write(self, text: str = "") -> None:
        self._progress_end()
        print(text)

    def progress(self, text: str) -> None:
        # only display if connected to terminal and enabled
        if (not Console.TERMINAL_CONNECTED) or (not Console.progress_enabled):
            return

        # fetch terminal dimensions
        max_width, _ = self._terminal_size()
        write_list = []

        if not Console._progress_active:
            # commence progress mode
            Console._progress_active = True
            write_list.append(Console.TERM_COLOR.YELLOW)

        # write progress message
        write_list.append(
            Console.CURSOR_START_LINE_CLEAR_RIGHT
            + self._text_truncated(text, max_width)
        )

        self._write_flush("".join(write_list))


def read_arguments(console: Console) -> tuple[str, bool, str]:
    # create argument parser
    parser = argparse.ArgumentParser(
        description="Recursively walk directory and generate ordered list of file path, filesize and SHA-1 hash."
    )

    parser.add_argument("scandir", help="source directory for scanning")

    parser.add_argument(
        "--progress", action="store_true", help="display activity during processing"
    )

    parser.add_argument(
        "--result-file", help="send results to file, rather than stdout"
    )

    arg_list = parser.parse_args()

    # ensure scandir exists
    scan_dir = arg_list.scandir.rstrip(os.sep)
    if not os.path.isdir(scan_dir):
        console.exit_error(f"invalid scan directory [{scan_dir}]")

    # if result file given, ensure parent path for file exists
    if arg_list.result_file is not None:
        check_dir = os.path.dirname(arg_list.result_file)
        if check_dir != "" and (not os.path.isdir(check_dir)):
            console.exit_error(
                f"nominated result file directory [{check_dir}] does not exist"
            )

    # return arguments
    return (scan_dir, arg_list.progress, arg_list.result_file)


def process_dir(
    console: Console, scan_dir: str
) -> tuple[int, list[tuple[str, int, str]]]:
    file_path_hash_list = []
    large_filesize = 0

    # walk starting `scan_dir`
    for dir_path, _, file_list in os.walk(scan_dir):
        for file_path in file_list:
            # build full path to next file
            file_path = os.path.join(dir_path, file_path)

            # get filesize of file - if not found (e.g. broken symlink) just silently move along as zero sized file
            filesize = 0
            try:
                filesize = os.path.getsize(file_path)
            except FileNotFoundError:
                # move along
                pass

            # keep track of largest filesize seen
            if filesize > large_filesize:
                large_filesize = filesize

            # SHA-1 hash file
            # note: no hashing for a zero length file
            file_hash = HASH_ZERO_FILE if (filesize == 0) else file_sha1_hash(file_path)

            # add completed item to list
            file_path_hash_list.append((file_path, filesize, file_hash))
            console.progress(f"{file_path} [{file_hash}]")

    # sort list by full file path and return
    file_path_hash_list.sort(key=lambda item: item[0])
    return (large_filesize, file_path_hash_list)


def file_sha1_hash(path: str) -> str:
    hasher = hashlib.sha1()
    fh = open(path, "rb")
    chunk = fh.read(HASH_FILE_CHUNK_SIZE)
    while chunk:
        hasher.update(chunk)
        chunk = fh.read(HASH_FILE_CHUNK_SIZE)

    fh.close()
    return hasher.hexdigest()


def generate_result(
    console: Console,
    result_file_path: str,
    high_filesize: int,
    file_path_hash_list: list,
) -> None:
    # determine string length of highest filesize to justify result lines
    filesize_pad = len(str(high_filesize))

    fh = None
    if result_file_path is not None:
        # write results to file
        fh = open(result_file_path, "w")

    for (file_path, filesize, file_hash) in file_path_hash_list:
        result_line = f"{file_hash}\t{str(filesize).rjust(filesize_pad)}\t{file_path}"

        if fh is not None:
            # send result to file
            fh.write(result_line + "\n")
            continue

        # send result to stdout
        console.write(f"{file_hash}\t{str(filesize).rjust(filesize_pad)}\t{file_path}")

    if fh is None:
        # extra linebreak
        console.write()
    else:
        fh.close()


def main():
    console = Console()

    # read CLI arguments
    scan_dir, Console.progress_enabled, result_file_path = read_arguments(console)

    # process scan directory
    large_filesize, file_path_hash_list = process_dir(console, scan_dir)

    # generate results
    generate_result(console, result_file_path, large_filesize, file_path_hash_list)

    # success
    console.write(f"Finished.\nTotal files: {len(file_path_hash_list)}")


if __name__ == "__main__":
    main()