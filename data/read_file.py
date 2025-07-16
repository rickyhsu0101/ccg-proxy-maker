import re
from typing import Tuple
from repository.card_db_repository import CardDbRepository

class CardListFileReader:
    def __init__(self):
        self.cardDbRepository = CardDbRepository()
    
    def parse_file_local(self, path: str, patternFormatter, lang: str):
        f = open(path, "r")
        lines = f.readlines()
        f.close()
        print([self.parse_line(line, lang) for line in lines])
        print([patternFormatter(series, sets, id) for series, sets, id in [self.parse_line(line, lang) for line in lines]])
        return [patternFormatter(series, sets, id) for series, sets, id in [self.parse_line(line, lang) for line in lines]]
    def parse_line(self, line: str, lang: str) -> Tuple[str, str, str] | None:
        match = re.match(r"([a-zA-Z]+)\/([a-zA-Z0-9]+)-([a-zA-Z0-9]+)", line)
        if match is None:
            return None
        cardInfo = (match.group(1).upper(), match.group(2).upper(), match.group(3).upper())
        if lang == "en":
            cardId = cardInfo[2]
            cardIdNumeric = re.findall(r"\d+", cardId)[0]
            if cardId[0] == "T":
                return (cardInfo[0], cardInfo[1], "TE"+cardIdNumeric)
            else:
                return (cardInfo[0], cardInfo[1], "E"+cardIdNumeric)
        return (match.group(1).upper(), match.group(2).upper(), match.group(3).upper())

    def parse_file(self, path: str, lang: str):
        f = open(path, "r")
        lines = f.readlines()
        f.close()
        return [self.cardDbRepository.get_card_url(cardInfo= (series, sets, id), lang=lang) for series, sets, id in [self.parse_line(line, lang) for line in lines]]
       


