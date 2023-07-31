import sys
import queue
import requests
import threading
import argparse
from requests.exceptions import HTTPError
from typing import List

def load_urls_from_file(filename: str) -> List[str]:
    """
    Load URLs from a file.

    Args:
        filename (str): Name of the file containing the URLs.

    Returns:
        List[str]: A list containing the URLs.
    """
    with open(filename, 'r') as file:
        return [line.strip() for line in file]

def get_queue(urls: List[str]) -> queue.Queue:
    """
    Create a queue of URLs.

    Args:
        urls (List[str]): A list of URLs.

    Returns:
        queue.Queue: A queue containing the URLs.
    """
    url_queue = queue.Queue()
    for url in urls:
        url_queue.put(url)
    return url_queue

def get_status(q: queue.Queue) -> None:
    """
    Check the HTTP status of a URL and log the status to stdout or stderr.

    Args:
        q (queue.Queue): The queue object that contains the URLs.
    """
    while not q.empty():
        url = q.get()
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
        except HTTPError:
            sys.stderr.write(f'HTTP error occurred for {url}\n')
            sys.stderr.flush()
        except Exception:
            sys.stderr.write(f'Error occurred for {url}\n')
            sys.stderr.flush()
        else:
            sys.stdout.write(f'Successfully connected to {url}\n')
            sys.stdout.flush()
        finally:
            q.task_done()

def check_website_status(url_queue: queue.Queue) -> None:
    """
    Create multiple threads to check the status of URLs in parallel.

    Args:
        url_queue (queue.Queue): A queue containing the URLs to check.
    """
    threads = []
    for _ in range(4):
        thread = threading.Thread(target=get_status, args=(url_queue,))
        thread.start()
        threads.append(thread)

    url_queue.join()

    for thread in threads:
        thread.join()

def parse_args() -> argparse.Namespace:
    """
    Parse command line arguments.

    Returns:
        argparse.Namespace: The parsed command line arguments.
    """
    parser = argparse.ArgumentParser(description="Website Status Checker Tool")
    parser.add_argument(
        "-i",
        "--input",
        help="File containing URLs to check their status.",
        required=False,
        default="urls.txt",
    )
    return parser.parse_args()

def main() -> None:
    """
    The main function to execute the website status checker tool.

    It loads URLs from a file, checks their status in parallel using multiple threads,
    and logs the status to stdout or stderr.
    """
    args = parse_args()
    urls = load_urls_from_file(args.input)
    url_queue = get_queue(urls)
    check_website_status(url_queue)

if __name__ == "__main__":
    main()
