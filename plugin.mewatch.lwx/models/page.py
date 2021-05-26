from typing import List
from models.episode import Episode

class Page:
    def __init__(self, **kwargs) -> None:
        self.title = kwargs['title']
        self.items = kwargs['items']