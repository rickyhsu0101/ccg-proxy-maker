from dataclasses import dataclass, field
from util.model.TextAnchor import TextAnchor
from data.model.WeissCardType import *
from typing import List, ClassVar


@dataclass
class CardData():
    series: str
    cardSet: str
    cardId: str
    
    cardAbility: List[str] = field(default_factory=lambda: [])
    url: str | None = None
    cardType: WeissCardType | None = None
    cardColor: WeissCardType | None = None

    textAnchor: TextAnchor = field(default_factory=lambda: TextAnchor())


DEFAULT_TEXT_ANCHOR = {
    WeissCardType.CHARACTER : TextAnchor(left=5, right=5, bottom=12),
    WeissCardType.EVENT: TextAnchor(left=5, right=5, bottom=9.5),
    WeissCardType.CLIMAX: TextAnchor(left=10, right=60, bottom=20)
}