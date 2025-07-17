from enum import Enum
from dataclasses import dataclass

class DocumentType(Enum):
    LETTER= 1
    A4= 2
    CUSTOM= 3


@dataclass
class DocumentInfo():
    dpi: int
    width: int
    height: int


DEFAULT_DPI = 300

DEFAULT_DOCUMENT_DIMS = {
    DocumentType.A4: DocumentInfo(300, 2480, 3508),
    DocumentType.LETTER: DocumentInfo(300, 2550-49, 3300-99),
    # DocumentType.LETTER: DocumentInfo(300, 2550-118, 3300-47),
    DocumentType.CUSTOM: DocumentInfo(300, 0, 0)
}