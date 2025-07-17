import re
from typing import Tuple, List
from repository.card_db_repository import CardDbRepository
from data.model.CardData import CardData
from util.model.TextAnchor import TextAnchor

class CardListFileReader:
    def __init__(self):
        self.cardDbRepository = CardDbRepository()
    def _create_text_anchor(self, parts=List[str]):
        anchor = TextAnchor()
        print("creating")
        if(len(parts[0]) > 0):
            try:
                print(parts[0])
                anchor.top = float(parts[0])
                # print("top")
            except Exception as e:
                print(f"{e} failed parse top")
        if(len(parts[1]) > 0):
            try:
                anchor.left = float(parts[1])
                # print("left")
            except Exception as e:
                print(f"{e} failed parse left")
        if(len(parts[2]) > 0):
            try:
                anchor.right = float(parts[2])
                # print("right")
            except Exception as e:
                print(f"{e} failed parse right")
        if(len(parts[3]) > 0):
            try:
                anchor.bottom = float(parts[3])
            except Exception as e:
                print(f"{e} failed parse bottom")
        return anchor
    def parse_file_csv(self, path: str, lang: str):
        f = open(path, "r")
        lines = f.readlines()
        f.close()
        # standardizedLines = [
        #     self.parse_line(cardInfo[0], lang)  
        #     for cardInfo in [(line.split(",")[0], line.split(",")[1])for line in lines] for _ in range(int(cardInfo[1]))]
        return [
            self.cardDbRepository.get_card_info(
                cardData=CardData(
                    series=lineParsed[0],
                    cardSet= lineParsed[1],
                    cardId= lineParsed[2],
                    textAnchor= self._create_text_anchor(lineSplit[3:7]) 
                        if len(lineSplit) >= 7 else 
                    TextAnchor()
                ), 
                lang=lang
            )
            for line in lines
            if (lineSplit := line.strip().split(",")) or True
            if (lineParsed :=  self.parse_line(lineSplit[0], lang)) or True
            for _ in range(int(lineSplit[1]))
        ]
        # return [self.cardDbRepository.get_card_url(cardInfo= (series, sets, id), lang=lang) for series, sets, id in standardizedLines]
    
    def parse_file_local(self, path: str, locaDb: dict[str, str], lang: str):
        f = open(path, "r")
        lines = f.readlines()
        f.close()
  
        return [
            self.cardDbRepository.get_card_info(
                cardData=CardData(
                    series=series,
                    cardSet= sets,
                    cardId= id,
                    url = locaDb[f"{series.upper()}/{sets.upper()}"].format(series, sets, id) 
                ), 
                lang=lang
            )
            (cardDetail := self.parse_line(line, lang)) for line in lines
            if(series:= cardDetail[0]) or True
            if(sets:= cardDetail[1]) or True
            if(id:= cardDetail[2]) or True
        ]
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
        return [
            self.cardDbRepository.get_card_info(
                cardData=CardData(
                    series=series,
                    cardSet= sets,
                    cardId= id
                ), 
                lang=lang
            )
            (cardDetail := self.parse_line(line, lang)) for line in lines
            if(series:= cardDetail[0]) or True
            if(sets:= cardDetail[1]) or True
            if(id:= cardDetail[2]) or True
        ]
        