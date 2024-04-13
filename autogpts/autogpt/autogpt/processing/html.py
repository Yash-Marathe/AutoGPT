"""HTML processing functions"""
from __future__ import annotations

import urllib.parse
from typing import List, Tuple, Union

from bs4 import BeautifulSoup
from requests.compat import urljoin


def extract_hyperlinks(soup: BeautifulSoup, base_url: str) -> List[Tuple[str, str]]:
    """Extract hyperlinks from a BeautifulSoup object

    Args:
        soup (BeautifulSoup): The BeautifulSoup object
        base_url (str): The base URL

    Returns:
        List[Tuple[str, str]]: The extracted hyperlinks
    """
    hyperlinks = []
    for link in soup.find_all("a", href=True):
        try:
            url = urljoin(base_url, link["href"])
        except urllib.parse.URLError:
            continue

        link_text = link.text.strip()
        if not link_text:
            continue

        hyperlinks.append((link_text, url))

    return hyperlinks


def format_hyperlink(link_text: str, link_url: str) -> str:
    """Format a single hyperlink to be displayed to the user

    Args:
        link_text (str): The text of the hyperlink
        link_url (str): The URL of the hyperlink

    Returns:
        str: The formatted hyperlink
    """
    max_length = 50
    if len(link_text) > max_length:
        link_text = f"{link_text[:max_length - 3]}..."

    return f
