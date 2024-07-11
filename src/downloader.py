"""Module for downloading content from a URL."""

import asyncio
import os

import aiohttp


async def fetch(session: aiohttp.ClientSession, url: str, dest: str) -> None:
    """
    Fetch content from the URL and save it to the destination.

    Args:
        session (aiohttp.ClientSession): The session for fetching.
        url (str): The URL to fetch the content from.
        dest (str): The destination file path to save the content.
    """
    async with session.get(url) as response:
        with open(dest, 'wb') as destination_file:
            chunk = await response.content.read(1024)
            while chunk:
                destination_file.write(chunk)
                chunk = await response.content.read(1024)


async def download_repo(repo_url: str, temp_dir: str) -> None:
    """
    Download repository contents into a temporary directory.

    Args:
        repo_url (str): The URL of the repository to download.
        temp_dir (str): The temporary directory to save the downloaded files.
    """
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    async with aiohttp.ClientSession() as session:
        tasks = []
        for index in range(3):
            dest = os.path.join(temp_dir, 'file_{0}.txt'.format(index))
            tasks.append(fetch(session, repo_url, dest))

        await asyncio.gather(*tasks)
