import json
import os

import requests
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.tools import tool

from linkedin_lookup.constants import (
    ENV_VAR_LINKEDIN_API_ENDPOINT,
    ENV_VAR_LINKEDIN_KEY,
)


@tool(parse_docstring=True)
def get_profile_url_tavily(name: str):
    """Use this tool to Searches for Linkedin Profile Url.

    Args:
        name (str): The name of the person
    """
    search = TavilySearchResults()
    res = search.run(f"{name}")
    return json.dumps(res, indent=4)


@tool(parse_docstring=True)
def scrape_linkedin_profile(linkedin_profile_url: str):
    """scrape information from LinkedIn profiles

    Args:
        linkedin_profile_url (str): the url of the linkedin profile to scrape
    """
    params = {
        "apikey": os.environ[ENV_VAR_LINKEDIN_KEY],
        "linkedInUrl": linkedin_profile_url,
    }
    response = requests.get(
        os.environ[ENV_VAR_LINKEDIN_API_ENDPOINT],
        params=params,
        timeout=10,
    )
    if not response.ok:
        response.raise_for_status()

    data = response.json().get("person")
    return data


def main_debug():
    a = get_profile_url_tavily.invoke({"name": "abdelmalek lamine linkedin"})
    print(a)
    b = scrape_linkedin_profile.invoke(
        {
            "linkedin_profile_url": "https://ch.linkedin.com/in/abdelmalek-lamine-160b36b9"
        }
    )


# if __name__ == "__main__":
#     main_debug()
