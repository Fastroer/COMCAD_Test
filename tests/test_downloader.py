"""Tests for the downloader module."""

import os

import pytest

from src.downloader import download_repo


@pytest.mark.asyncio()
async def test_download_repo():
    """
    Test the download_repo function for asynchronous repo downloading.

    Steps:
    1. Create a temporary directory for downloading files.
    2. Asynchronously download the content of the repo.
    3. Check that the temporary directory exists.
    4. Check that the temporary directory contains 3 files.
    5. Check that each of the 3 files is indeed a file.
    6. Remove all files and the temporary directory after the test.
    """
    temp_dir = 'test_tmp'
    try:
        await download_repo(
            'https://gitea.radium.group/radium/project-configuration',
            temp_dir,
        )
    finally:
        if os.path.exists(temp_dir):
            assert os.path.exists(temp_dir), 'Temp directory was not created'
            assert len(os.listdir(temp_dir)) == 3, (
                'Number of files in the temp directory is not 3'
            )
            for file_name in os.listdir(temp_dir):
                assert os.path.isfile(os.path.join(temp_dir, file_name)), (
                    '{0} is not a file'.format(file_name)
                )
            for fname in os.listdir(temp_dir):
                os.remove(os.path.join(temp_dir, fname))
            os.rmdir(temp_dir)
