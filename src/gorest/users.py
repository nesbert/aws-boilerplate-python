from typing import Optional

import logging
import requests

from gorest import BASE_URL
from gorest import READ_TIMEOUT

RESOURCE_URL = f"{BASE_URL}/v2/users"


def fetch(user_id: int):
    response = requests.get(f"{RESOURCE_URL}/{user_id}", timeout=READ_TIMEOUT)
    response.raise_for_status()
    return response.json()


def fetch_all(page: Optional[int] = None, limit: Optional[int] = None):
    query = {
        param: value
        for param, value in [("page", page), ("per_page", limit)]
        if value is not None
    }
    logging.debug("url=%s, query=%s", RESOURCE_URL, query)
    response = requests.get(RESOURCE_URL, params=query, timeout=READ_TIMEOUT)
    response.raise_for_status()
    return response.json()
