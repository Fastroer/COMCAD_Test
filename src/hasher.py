"""Module for computing SHA256 hashes of files in a directory."""

import hashlib
import os
from typing import BinaryIO, Dict, Generator


def read_file_in_chunks(
    file_obj: BinaryIO,
    size: int,
) -> Generator[bytes, None, None]:
    """
    Read file in chunks of given size.

    Args:
        file_obj (BinaryIO): The file object to read from.
        size (int): The size of each chunk to read.

    Yields:
        bytes: The next chunk of the file.
    """
    chunk = file_obj.read(size)
    while chunk:
        yield chunk
        chunk = file_obj.read(size)


def compute_file_hash(file_path: str, block_size: int = 4096) -> str:
    """
    Compute SHA256 hash of a single file.

    Args:
        file_path (str): The path to the file.
        block_size (int): The size of each chunk to read.

    Returns:
        str: The SHA256 hash of the file.
    """
    sha256_hash = hashlib.sha256()
    with open(file_path, 'rb') as file_obj:
        for byte_block in read_file_in_chunks(file_obj, block_size):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()


def get_files_in_directory(directory: str) -> list[str]:
    """
    Get all file paths in the given directory.

    Args:
        directory (str): The directory to scan for files.

    Returns:
        list: A list of file paths.
    """
    file_paths = []
    for root, _, files in os.walk(directory):
        for file_name in files:
            file_paths.append(os.path.join(root, file_name))
    return file_paths


def compute_hashes(directory: str) -> Dict[str, str]:
    """
    Compute SHA256 hash of each file in the given directory.

    Args:
        directory (str): The directory to scan for files.

    Returns:
        dict: A dictionary with filenames as keys, SHA256 hashes as values.
    """
    file_hashes = {}
    for file_name in get_files_in_directory(directory):
        file_hashes[file_name] = compute_file_hash(file_name)
    return file_hashes
