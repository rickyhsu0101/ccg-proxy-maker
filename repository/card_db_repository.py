import requests
import json
import os
from typing import Tuple
from data.model.WeissCardType import WeissCardType
from data.model.WeisCardColor import WeissCardColor
from data.model.CardData import CardData
from itertools import groupby

jp_base = {
    "DAL/W131": {
        "DAL/W131-P05S": {
            "ability": [
                "AUTO: At the beginning of your opponent's draw phase, choose 1 of your characters, and that character gets +1500 power until the end of the turn.",
                "AUTO: During your opponent's turn, when your opponent's character becomes reversed, look at the top of your deck, and put it on the top or at the bottom of your deck."
            ],
            "color": "blue",
            "type": "character",
            "image": "https://ws-tcg.com/wordpress/wp-content/images/cardlist/d/dal_w131/dal_w131_p05s.png"
        }
    },
    "SBY/W136": {
        "SBY/W136-043R": {
            "ability": [
                "【永】 あなたのキャラすべてに、パワーを＋1000し、ソウルを＋1。",
                "（[TREASURE]：このカードがトリガーした時、あなたはこのカードを手札に戻す。あなたは自分の山札の上から1枚を、ストック置場に置いてよい）"
            ],
            "color": "green",
            "type": "climax",
            "image": "https://ws-tcg.com/wordpress/wp-content/images/cardlist/s/sby_w136/sby_w136_043r.png"
        },
        "SBY/W136-044R": {
            "ability": [
                "【永】 あなたのキャラすべてに、パワーを＋1000し、ソウルを＋1。",
                "（[TREASURE]：このカードがトリガーした時、あなたはこのカードを手札に戻す。あなたは自分の山札の上から1枚を、ストック置場に置いてよい）"
            ],
            "color": "green",
            "type": "climax",
            "image": "https://ws-tcg.com/wordpress/wp-content/images/cardlist/s/sby_w136/sby_w136_044r.png"
        }
    }
}

class CardDbRepository():
    EN_DB_URL = "https://raw.githubusercontent.com/CCondeluci/WeissSchwarz-ENG-DB/refs/heads/master/DB/{series}_{cardSet}.json"
    JP_DB_URL = "https://raw.githubusercontent.com/CCondeluci/WeissSchwarz-JP-DB/refs/heads/main/DB/{series}_{cardSet}.json"
    def __init__(self):
        self.db = dict()
    def _get_set_info(self, series: str, cardSet: str, lang: str, localJPDb: list[object] = []):
        card_list = localJPDb
        rtext = ""
        try:
            if len(localJPDb) == 0: 
                url = CardDbRepository.JP_DB_URL if lang == "jp" else CardDbRepository.EN_DB_URL
                r = requests.get(url.format(
                    series= series.upper(),
                    cardSet= cardSet.upper()
                ))
                rtext = r.text
                card_list = json.loads(r.text)
        except Exception as e:
            print(rtext)
        
        self.db[f"{series}/{cardSet}"] = {card["code"]: card for card in card_list}
    def get_card_url(self, cardInfo: Tuple[str, str, str], lang = "jp")->str:
        series, cardSet, id = cardInfo

        if f"{series}/{cardSet}" not in self.db:
            self._get_set_info(series, cardSet, lang)

        return self.db[f"{series}/{cardSet}"][f"{series}/{cardSet.upper()}-{id.upper()}"]["image"]
    def get_card_info(self, cardData: CardData, lang = "jp") -> CardData:
        base = jp_base
        series = cardData.series
        cardSet = cardData.cardSet
        cardId = cardData.cardId

        seriesUpper = "".join([c for c in series if c.isupper()])

        if f"{seriesUpper}/{cardSet}" not in self.db:
            localJpDb = self._checkLocalJpDb(
                series = seriesUpper, 
                cardSet = cardSet
            ) if lang == "jp" else []
            self._get_set_info(seriesUpper, cardSet, lang, localJpDb)
            if f"{seriesUpper}/{cardSet}" in base:
                self.db[f"{seriesUpper}/{cardSet}"] = {**self.db[f"{seriesUpper}/{cardSet}"], **base[f"{seriesUpper}/{cardSet}"]}
        
        jsonObject = self.db[f"{seriesUpper}/{cardSet}"][f"{series}/{cardSet.upper()}-{cardId.upper()}"]
        cardData.cardAbility = jsonObject["ability"]
        cardData.cardColor = WeissCardColor[jsonObject["color"].upper()]
        cardData.cardType = WeissCardType[jsonObject["type"].upper()]
        if cardData.url is None:
            cardData.url = jsonObject["image"]

        return cardData
    def _checkLocalJpDb(self, series: str, cardSet: str) -> list[object]:
        jsonObjectList = []
        if os.path.exists(f"./data/jpdb/{series.upper()}_{cardSet.upper()}.json"): 
            with open(f"./data/jpdb/{series.upper()}_{cardSet.upper()}.json", "r") as f:
                jsonObjectList = json.load(f)
                f.close()
        print(f"jsonJPDB ./data/jpdb/{series.upper()}_{cardSet.upper()} len: {len(jsonObjectList)}")
        return jsonObjectList