from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from lagent.schema import ActionReturn


@dataclass
class WMemoryItem(ActionReturn):
    pass


class WorkingMemory(ABC):

    def __init__(self) -> None:
        super().__init__()
        self.data = None

    @abstractmethod
    def query(self, query_item: ActionReturn):
        """
        Query the working memory to return data based on the query item.
        The query item 
        
        Args:
            query_item (ActionReturn): Query item, which defines what items are returned
            by this function.
        """
        pass

    @abstractmethod
    def add(self, item:ActionReturn):
        pass