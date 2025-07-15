import requests
import json
from typing import Tuple

class CardDbRepository():
    EN_DB_URL = "https://raw.githubusercontent.com/CCondeluci/WeissSchwarz-ENG-DB/refs/heads/master/DB/{series}_{cardSet}.json"
    JP_DB_URL = "https://raw.githubusercontent.com/CCondeluci/WeissSchwarz-JP-DB/refs/heads/main/DB/{series}_{cardSet}.json"
    def __init__(self):
        self.db = dict()
    def _get_set_info(self, series: str, cardSet: str, lang: str):
        url = CardDbRepository.JP_DB_URL if lang == "jp" else CardDbRepository.EN_DB_URL
        r = requests.get(url.format(
            series= series.upper(),
            cardSet= cardSet.upper()
        ))
        card_list = json.loads(r.text)
        self.db[f"{series}/{cardSet}"] = {card["code"]: card for card in card_list}
    def get_card_url(self, cardInfo: Tuple[str, str, str], lang = "jp")->str:
        series, cardSet, id = cardInfo

        if f"{series}/{cardSet}" not in self.db:
            self._get_set_info(series, cardSet, lang)

        return self.db[f"{series}/{cardSet}"][f"{series}/{cardSet.upper()}-{id.upper()}"]["image"]
