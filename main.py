"""Main script to download a repository and compute file hashes."""

import asyncio
import logging
import os

from src.downloader import download_repo
from src.hasher import compute_hashes

logging.basicConfig(
    level=logging.INFO,
    format='{asctime} - {levelname} - {message}',
    style='{'
)


async def main() -> None:
    """
    Download a repository and compute SHA256 hashes of its files.

    Steps:
    1. Define the repository URL and a temporary directory for downloading.
    2. Download the repository content into the temporary directory.
    3. Compute SHA256 hashes of the downloaded files.
    4. Remove all files and the temporary directory after computing the hashes.
    """
    repo_url = 'https://gitea.radium.group/radium/project-configuration'
    temp_dir = 'tmp'

    try:
        await download_repo(repo_url, temp_dir)
    except Exception as error:
        log_error('An error occurred during download: {0}'.format(error))
        return

    try:
        hashes = compute_hashes(temp_dir)
    except Exception as hash_error:
        log_error(
            'An error occurred during hash computation: {0}'.format(hash_error)
        )
        return

    for file_name, hash_value in hashes.items():
        log_info('{0}: {1}'.format(file_name, hash_value))

    clean_temp_dir(temp_dir)


def log_error(message: str) -> None:
    """Log an error message."""
    logging.error(message)


def log_info(message: str) -> None:
    """Log an informational message."""
    logging.info(message)


def clean_temp_dir(directory: str) -> None:
    """Remove all files and the directory."""
    if os.path.exists(directory):
        for file_name in os.listdir(directory):
            os.remove(os.path.join(directory, file_name))
        os.rmdir(directory)


if __name__ == '__main__':
    asyncio.run(main())
