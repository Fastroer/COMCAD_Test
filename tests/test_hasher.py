"""Tests for the hasher module."""

import os

from src.hasher import compute_hashes


def test_compute_hashes():
    """
    Tests the compute_hashes function for computing file hashes.

    This test performs the following steps:
    1. Creates a temporary directory.
    2. Creates a temporary file 'test.txt' with content 'test content'.
    3. Calls the compute_hashes function to compute the file's hash.
    4. Checks that the file 'test.txt' is included in the hash results.
    5. Removes the temporary file and directory after the test.

    If all checks pass, the test is considered successful.
    """
    temp_dir = 'test_tmp'
    os.makedirs(temp_dir)
    test_file_path = os.path.join(temp_dir, 'test.txt')
    with open(test_file_path, 'w') as file_obj:
        file_obj.write('test content')

    hashes = compute_hashes(temp_dir)
    assert hashes is not None, 'compute_hashes function returned None'
    assert test_file_path in hashes, (
        'File {0} was not found in the hash results'.format(test_file_path)
    )

    if os.path.exists(test_file_path):
        os.remove(test_file_path)
    if os.path.exists(temp_dir):
        os.rmdir(temp_dir)
