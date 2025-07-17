from dataclasses import dataclass
from typing import Tuple

@dataclass
class TextBound():
    topLeft: Tuple[int, int] | None = None
    #topRight: Tuple[int, int] | None
    #bottomRight: Tuple[int, int] | None
    bottomRight: Tuple[int, int] | None = None
    width: int | None = None

    def is_drawable(self):
        if(self.width is None):
            return False
        if(self.topLeft is None and self.bottomRight is None):
            return False
        return True