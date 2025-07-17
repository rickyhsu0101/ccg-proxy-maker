from dataclasses import dataclass
from util.model.TextBound import TextBound

@dataclass
class TextAnchor():
    top: float | None = None
    left: float | None = None
    right: float | None = None
    bottom: float | None = None
    

    def compute_text_bound(self, width: int, height: int) -> TextBound | None:
        if(
            self.top is None and 
            self.left is None and 
            self.right is None and
            self.bottom is None
        ):
            return None
        textBound: TextBound = TextBound()
        if(self.top is not None and self.left is not None):
            textBound.topLeft = (
                int(width / 100 * self.left), 
                int(height / 100 * self.top)
            )
        if(self.right is not None and self.bottom is not None):
            textBound.bottomRight = (
                int(width - (width / 100 * self.right)),
                int(height - (height / 100 * self.bottom))
            )
        if(self.left is not None and self.right is not None):
            textBound.width = width - width * (self.left + self.right) / 100
        return textBound
