from typing import Any, List

from linkedin_lookup.tools.tools import get_profile_url_tavily, scrape_linkedin_profile
from linkedin_lookup.types import ToolType


def get_all_tools() -> List[ToolType]:
    return [get_profile_url_tavily, scrape_linkedin_profile]
