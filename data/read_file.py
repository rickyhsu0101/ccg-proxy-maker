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
    def parse_file_comb(self, path: str, locaDb: dict[str, str], needExternalSource: bool = True):
        f = open(path, "r")
        lines = f.readlines()
        f.close()
        return [
            self.cardDbRepository.get_card_info(
                cardData=CardData(
                    series=lineParsed[0],
                    cardSet= lineParsed[1],
                    cardId= lineParsed[2],
                    textAnchor= self._create_text_anchor(lineSplit[4:8]) 
                        if len(lineSplit) >= 8 else 
                        TextAnchor(),
                    translate= lineSplit[8] != "NT"
                        if len(lineSplit) >=9 else
                        True
                 ), 
                lang="jp"
            ) if lineSplit[0] == 'JP' else
            self.cardDbRepository.get_card_info(
                cardData=CardData(
                    series= lineParsed[0],
                    cardSet= lineParsed[1],
                    cardId= lineParsed[2],
                    url = locaDb[f"{lineParsed[0]}/{lineParsed[1].upper()}"].format(str(lineParsed[2])) 
                ), 
                lang="en"
            ) if needExternalSource else CardData(
                series=lineParsed[0],
                cardSet= lineParsed[1],
                cardId= lineParsed[2],
                url = locaDb[f"{lineParsed[0]}/{lineParsed[1].upper()}"].format(str(lineParsed[2])) 
            )
            for line in lines
            if (lineSplit := line.strip().split(",")) or True
            if (lineParsed :=  self.parse_line(lineSplit[1], lineSplit[0].lower())) or True
            for _ in range(int(lineSplit[2]))
        ]
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
                        TextAnchor(),
                    translate= lineSplit[7] != "NT"
                        if len(lineSplit) >=8 else
                        True
                 ), 
                lang=lang
            )
            for line in lines
            if (lineSplit := line.strip().split(",")) or True
            if (lineParsed :=  self.parse_line(lineSplit[0], lang)) or True
            for _ in range(int(lineSplit[1]))
        ]
        # return [self.cardDbRepository.get_card_url(cardInfo= (series, sets, id), lang=lang) for series, sets, id in standardizedLines]
    
    def parse_file_local(self, path: str, locaDb: dict[str, str], lang: str, needExternalSource: bool = True):
        f = open(path, "r")
        lines = f.readlines()
        f.close()
        # cardDetail: Tuple[str, str, str] = ()
        # print(cardDetail)
        return [
            self.cardDbRepository.get_card_info(
                cardData=CardData(
                    series=series,
                    cardSet= sets,
                    cardId= id,
                    url = locaDb[f"{series}/{sets.upper()}"].format(str(id)) 
                ), 
                lang=lang
            ) if needExternalSource else CardData(
                series=series,
                cardSet= sets,
                cardId= id,
                url = locaDb[f"{series}/{sets.upper()}"].format(str(id)) 
            )
            for line in lines
            if (cardDetail := self.parse_line(line, lang))  or True
            if(series:= cardDetail[0]) or True
            if(sets:= cardDetail[1]) or True
            if(id:= cardDetail[2]) or True
        ]
    def parse_line(self, line: str, lang: str) -> Tuple[str, str, str] | None:
        match = re.match(r"([a-zA-Z\d]+)\/([a-zA-Z0-9]+)-([a-zA-Z0-9]+[a-zA-Z@]*)", line)
        if match is None:
            return None
        cardInfo = (match.group(1), match.group(2), match.group(3))
        if lang == "en":
            cardId = cardInfo[2]
            cardIdNumeric = re.findall(r"\d+[a-zA-Z]*", cardId)[0]
            if cardId[0] == "T":
                return (cardInfo[0], cardInfo[1], "TE"+cardIdNumeric)
            if cardId[0] == "P":
                return (cardInfo[0], cardInfo[1], "PE"+cardIdNumeric)
            else:
                return (cardInfo[0], cardInfo[1], "E"+cardIdNumeric)
        print((match.group(1), match.group(2), match.group(3)))
        return (match.group(1), match.group(2), match.group(3))

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
        