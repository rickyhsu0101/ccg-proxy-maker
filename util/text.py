from typing import List, Tuple, Self
from PIL import ImageDraw, ImageFont, Image
from PIL.ImageFont import FreeTypeFont
from data.model.CardData import CardData, DEFAULT_TEXT_ANCHOR
from util.model.TextBound import TextBound
# from data.model.WeisCardColor import WeissCardColor
from data.model.WeissCardType import WeissCardType
class CardText():
    def __init__(self):
        self.texts: List[str] = []
        self.font: FreeTypeFont = ImageFont.truetype("Arial.ttf", 20)
        self.fontSize: int = 20
        self.spacing: int = 8
        self.line_padding: int = 4
    def set_texts(self, texts: List[str]):
        self.texts = texts
        return self
    def set_font_size(self, fontSize: int):
        self.font = ImageFont.truetype("arial.ttf", fontSize)
        self.fontSize = fontSize
        return self
    def set_spacing(self, spacing: int):
        self.spacing = spacing
        return self
    def set_line_pading(self, padding):
        self.line_padding = padding
        return self
    def _calculate_sizes(self):
        wordsLists = [text.split(" ") for text in self.texts]
        return [
            [
                (
                    wordWithSpace,
                    self.font.getlength(wordWithSpace)
                ) 
                for ind, word in enumerate(wordsList)
                if(wordWithSpace := word + (" " if ind != len(wordsList) - 1 else ""))
            ]
            for wordsList in wordsLists
        ]
    def _determine_multiline_texts(self, width: int) -> List[List[str]]:
        textsSizes = self._calculate_sizes()
        # print("textsSizes")
        # print(textsSizes)
        multiLineTexts: List[List[str]] = [ [""] for _ in textsSizes]
        current: int = 0
        lineInd: int = 0

        def appendValue(textInd: int, lineInd: int, word: str):
            # print("appended")
            multiLineTexts[textInd][lineInd] += word
        [
            (
                (
                    appendValue(textInd, lineInd, wordInfo[0]), 
                    current := current + wordInfo[1],
                ) 
                if current + wordInfo[1] < width else
                (
                    multiLineTexts[textInd].append(wordInfo[0]),
                    current := wordInfo[1],
                    lineInd := lineInd + 1
                )
            )
            for textInd, wordsSizes in enumerate(textsSizes)
            if (current := 0) or True
            if (lineInd := 0) or True
            for wordInfo in wordsSizes
        ]
        return multiLineTexts
    def _flatten_multiline_texts(self, multiline_texts: List[List[str]]) -> List[str]:
        return [
            line
            for text in multiline_texts
            for line in text
        ]
    def _combine_multiline(self, multiline_texts: List[List[str]]):
        "\n".join([
            "\n".join(text)
            for text in multiline_texts
        ])
    def _determine_height(self, multiline_texts: List[List[str]]) -> int:
        height: int = 0
        [
            (height := height + len(text) * (self.fontSize + self.spacing + 2*self.line_padding), print(height))
            for text in multiline_texts
        ]
        return height - self.spacing
    def _draw_text_background(self, draw: ImageDraw.ImageDraw, text: str, loc: Tuple[int, int], cardColor: str):
        length: int = int(
            draw.textlength(
                text = text,
                font = self.font
            )
        )
        draw.rectangle(
            xy = [
                loc,
                (
                    loc[0] + length + 2 * self.line_padding,
                    loc[1] + self.fontSize + 2 * self.line_padding
                )
            ],
            fill = cardColor,
            width = 0
        )
    def _draw_text(self, draw: ImageDraw.ImageDraw, text: str, loc: Tuple[int, int]):
        draw.text(
            xy = (loc[0]+self.line_padding, loc[1] + self.line_padding),
            text = text,
            font = self.font,
            fill= "white",
            stroke_width=2,
            stroke_fill="black"
        )
    def _update_start_point(self, point: Tuple[int, int]):
        return (
            point[0],
            point[1] + self.fontSize + 2 * self.line_padding + self.spacing
        )
    def draw_text(self, image: Image.Image, cardData: CardData):
        textBound: TextBound = cardData.textAnchor.compute_text_bound(
            width = image.width, 
            height = image.height
        )
        if(cardData.cardType == WeissCardType.CLIMAX):
            return
        # if cardData.cardId == "049":
        #     print(cardData.textAnchor)
        #     print(textBound)
        #print(cardData)
        if(textBound is None):
            textBound = DEFAULT_TEXT_ANCHOR[cardData.cardType].compute_text_bound(
                width = image.width, 
                height = image.height
            )
        if(not textBound.is_drawable()):
            return
        self.texts = cardData.cardAbility
        # print(cardData.cardAbility)
        # print("mode")
        # print(image.mode)
        
        draw: ImageDraw.ImageDraw  = ImageDraw.Draw(image)

        multiline_texts: List[List[str]] = self._determine_multiline_texts(textBound.width - 2 * self.line_padding)
        height: int = self._determine_height(multiline_texts)
        lines: List[str] = self._flatten_multiline_texts(multiline_texts)

        startPoint: Tuple[int, int] = (0,0)
        if(textBound.topLeft is not None):
            startPoint = textBound.topLeft
        else:
            startPoint = (
                textBound.bottomRight[0] - textBound.width,
                textBound.bottomRight[1] - height
            )
        point: Tuple[int, int] = startPoint
        print(startPoint)
        print(multiline_texts)
        print(len(lines))
        print(height)
        print(textBound)
        [
            (
                self._draw_text_background(
                    draw = draw,
                    text = line,
                    loc = point,
                    cardColor = cardData.cardColor.name
                ), 
                self._draw_text(
                    draw = draw,
                    text = line,
                    loc = point
                ),
                point := self._update_start_point(point)
            )
            for line in lines
        ]