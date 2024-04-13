from __future__ import annotations

import json
import time
from itertools import islice
from typing import List, Union

from duckduckgo_search import DDGS
from ..registry import action

DUCKDUCKGO_MAX_ATTEMPTS = 3


@action(
    name="web_search",
    description="Searches the web",
    parameters=[
        {
            "name": "query",
            "description": "The search query",
            "type": "string",
            "required": True,
        }
    ],
    output_type=List[str],
)
async def web_search(agent, task_id: str, query: str) -> List[str]:
    """Return the results of a web search

    Args:
        query (str): The search query.
        num_results (int): The number of results to return.

    Returns:
        List[str]: The results of the search.
    """
    search_results = []
    attempts = 0
    num_results = 8

    while attempts < DUCKDUCKGO_MAX_ATTEMPTS:
        if not query:
            return search_results

        try:
            results = DDGS().text(query)
            search_results = list(islice(results, num_results))

            if search_results:
                break

        except Exception as e:
            print(f"Error: {e}")

        time.sleep(1)
        attempts += 1

    if not search_results:
        raise Exception("Failed to retrieve search results")

    return search_results


def safe_google_results(results: Union[str, List[str]]) -> List[str]:
    """
    Return the results of a web search in a safe format.

    Args:
        results (str | list): The search results.

    Returns:
        List[str]: The results of the search.
    """
    if isinstance(results, str):
        try:
            results = json.loads(results)
            return [result.encode("utf-8", "ignore").decode("utf-8") for result in results]
        except Exception as e:
            print(f"Error: {e}")
            return []

    elif isinstance(results, list):
        return [result.encode("utf-8", "ignore").decode("utf-8") for result in results]

    else:
        return []
