from typing import Any

from lagent.schema import ActionReturn
from agent.abstract.working_memory import WorkingMemory


class WorkingMemory(WorkingMemory):
    """
    My custom working memory class.
    """
    def __init__(self) -> None:
        """
        Initialize the working memory.
        """
        pass
    
    def query(self, query_item: ActionReturn) -> Any:
        """
        Query the working memory.

        Parameters:
            query_item (ActionReturn): Item to query.

        Returns:
            Any: Query result.
        """
        pass

    def add(self, item) -> None:
        """
        Add an item to the working memory.

        Parameters:
            item (ActionReturn): Item to add.
        """
        pass