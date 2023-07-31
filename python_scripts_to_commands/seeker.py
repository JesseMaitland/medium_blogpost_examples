import sys
from typing import Iterable
from pathlib import Path
from argparse import ArgumentParser, Namespace


def search_for_files(path: Path, extension: str) -> Iterable[Path]:
    """
    Search for files recursively from a given path based on file extension.

    Args:
        path (Path): The base path to start searching.
        extension (str): The file extension to search for.

    Yields:
        Paths of the files found with the provided file extension.
    """
    for path in path.glob(f"**/*.{extension}"):
        yield path


def write_to_stdout(index: int, file_path: Path, template: str) -> None:
    """
    Writes formatted output to stdout.

    Args:
        index (int): The index of the current file.
        file_path (Path): The path of the current file.
        template (str): The format string used to print the output.
    """
    sys.stdout.write(template.format(index=index, file_path=file_path))
    sys.stdout.flush()


def get_output_string_template(index: bool) -> str:
    """
    Returns a format string based on the given index flag.

    Args:
        index (bool): If true, includes the file index in the format string.

    Returns:
        A format string to be used for output.
    """
    if index:
        return "{index}: {file_path} \n"
    return "{file_path} \n"


def write_to_stderr_and_exit(extension: str) -> None:
    """
    Writes an error message to stderr and exits the program with a status code of 1.

    Args:
        extension (str): The file extension that was being searched for.
    """
    sys.stderr.write(f"Error: No Files Found with extension .{extension}")
    sys.stderr.flush()
    exit(1)


def sanitize_extension(extension: str) -> str:
    """
    Sanitizes the file extension input by removing the leading dot if it exists.

    Args:
        extension (str): The file extension input from the user.

    Returns:
        The sanitized file extension.
    """
    return extension.lstrip(".")


def parse_args() -> Namespace:
    """
    Parses command line arguments.

    Returns:
        An argparse.Namespace containing the parsed arguments.
    """
    parser = ArgumentParser()
    parser.add_argument("extension", type=str, help="The extension to search for without the preceding (.) dot .")
    parser.add_argument("--index", "-i", help="Print the index of the file", action="store_true")
    return parser.parse_args()


def main() -> None:
    """
    The main function of the script. It parses arguments, searches for files with the specified extension,
    writes the results to stdout, and handles the case where no files were found.
    """

    args = parse_args()
    extension = sanitize_extension(args.extension)

    path = Path.cwd()
    file_count = 0
    template = get_output_string_template(args.index)

    for file_path in search_for_files(path, extension):
        file_count += 1
        write_to_stdout(file_count, file_path, template)

    if file_count == 0:
        write_to_stderr_and_exit(args.extension)


if __name__ == "__main__":
    main()
