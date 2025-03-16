from typing import Callable, Union

from langchain_core.runnables import Runnable
from langchain_core.tools.base import BaseTool

ToolType = Union[
    BaseTool,
    Callable[[Union[Callable, Runnable]], BaseTool],
]
