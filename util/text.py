from typing import List, Tuple, Self
from PIL import ImageDraw, ImageFont, Image, ImageColor
from PIL.ImageFont import FreeTypeFont
from data.model.CardData import CardData, DEFAULT_TEXT_ANCHOR
from util.model.TextBound import TextBound
from data.model.WeisCardColor import WeissCardColor
from data.model.WeissCardType import WeissCardType
class CardText():
    def __init__(self):
        self.texts: List[str] = []
        self.font: FreeTypeFont = ImageFont.truetype("DejaVuSans.ttf", 20)
        self.fontSize: int = 20
        self.spacing: int = 8
        self.line_padding: int = 4
        self.stroke_width: int = 2
        self.outline_rect: bool = False
        self.full_background: bool = False
    def set_outline_rect(self, outline_rect):
        self.outline_rect = outline_rect
        return self
    def set_full_background(self, full_background):
        self.full_background = full_background
        return self
    def set_texts(self, texts: List[str]):
        self.texts = texts
        return self
    def set_font_size(self, fontSize: int):
        self.font = ImageFont.truetype("DejaVuSans.ttf", fontSize)
        self.fontSize = fontSize
        return self
    def set_spacing(self, spacing: int):
        self.spacing = spacing
        return self
    def set_stroke_width(self, width: int):
        self.stroke_width = width
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
        #print(cardColor)
        
        color = ImageColor.getrgb(cardColor)
        if cardColor.lower() == "yellow":
            color = "orange"
        if cardColor.lower() == "blue":
            color = ImageColor.getrgb("#0076c0")
        if cardColor.lower() == "red":
            color = ImageColor.getrgb("#b31f1d")
        # print(color)
        # print(self.outline_rect)
        # exit(1)

        opacity = 0.7
        draw.rectangle(
            xy = [
                (
                    loc[0] - (4 if self.outline_rect else 0),
                    loc[1] - (4 if self.outline_rect else 0)
                ),
                (
                    loc[0] + length + 2 * self.line_padding + (4 if self.outline_rect else 0),
                    loc[1] + self.fontSize + 2 * self.line_padding + (4 if self.outline_rect else 0)
                )
            ],
            fill = (211,211,211) + (int(255*opacity),),
            # fill = ImageColor.getrgb(cardColor) + (int(255*opacity),),
            outline = color if self.outline_rect else None,
            width = 4 if self.outline_rect else 0
        )
    def _draw_full_text_background(self, draw: ImageDraw.ImageDraw, start: Tuple[int, int], end: Tuple[int, int], cardColor: str):
        opacity = 0.7
        color = ImageColor.getrgb(cardColor)
        if cardColor.lower() == "yellow":
            color = "orange"
        if cardColor.lower() == "blue":
            color = ImageColor.getrgb("#006aac")
        if cardColor.lower() == "red":
            color = ImageColor.getrgb("#c72321")
        draw.rectangle(
            xy = [
                (
                    start[0] - (10 if self.outline_rect else 0),
                    start[1] - (10 if self.outline_rect else 0)
                ),
                (
                    end[0] + (10 if self.outline_rect else 0),
                    end[1] + (10 if self.outline_rect else 0)
                ),
            ],
            fill = (211,211,211) + (int(255*opacity),),
            # fill = ImageColor.getrgb(cardColor) + (int(255*opacity),),
            outline = color if self.outline_rect else None,
            width = 10 if self.outline_rect else 0
        )
    def _draw_text(self, draw: ImageDraw.ImageDraw, text: str, loc: Tuple[int, int], color: WeissCardColor):
        # fill: str = "white"
        # stroke: str = "white"
        # if (color == WeissCardColor.YELLOW):
        #     fill = "black"
        #     stroke = "black"
        fill: str = "black"
        stroke: str = "black"
        draw.text(
            xy = (loc[0]+self.line_padding, loc[1] + self.line_padding),
            text = text,
            font = self.font,
            fill= fill,
            stroke_width=self.stroke_width,
            stroke_fill=stroke
        )
    def _update_start_point(self, point: Tuple[int, int]):
        return (
            point[0],
            point[1] + self.fontSize + 2 * self.line_padding + self.spacing
        )
    def draw_text(self, image: Image.Image, cardData: CardData) -> Image.Image:
        textBound: TextBound = cardData.textAnchor.compute_text_bound(
            width = image.width, 
            height = image.height
        )
        if(cardData.cardType == WeissCardType.CLIMAX):
            return image
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
            return image
        self.texts = cardData.cardAbility
        # print(cardData.cardAbility)
        # print("mode")
        # print(image.mode)
        
        draw: ImageDraw.ImageDraw  = ImageDraw.Draw(image)

        multiline_texts: List[List[str]] = self._determine_multiline_texts(textBound.width - 2 * self.line_padding)
        height: int = self._determine_height(multiline_texts)
        lines: List[str] = self._flatten_multiline_texts(multiline_texts)

        startPoint: Tuple[int, int] = (0,0)
        endPoint: Tuple[int, int] = (0,0)
        if(textBound.topLeft is not None):
            startPoint = textBound.topLeft
            endPoint = (startPoint[0] + textBound.width, startPoint[1] + height)
        else:
            startPoint = (
                textBound.bottomRight[0] - textBound.width,
                textBound.bottomRight[1] - height
            )
            endPoint = textBound.bottomRight
        point: Tuple[int, int] = startPoint
        print(startPoint)
        print(multiline_texts)
        print(len(lines))
        print(height)
        print(textBound)
        overlay = Image.new('RGBA', image.size, (255,255,255,0))
        overlayDraw = ImageDraw.Draw(overlay)
        if self.full_background:
            self._draw_full_text_background(
                draw = overlayDraw,
                start = startPoint,
                end = endPoint,
                cardColor = cardData.cardColor.name
            )
        else:
            [
                (
                    self._draw_text_background(
                        draw = overlayDraw,
                        text = line,
                        loc = point,
                        cardColor = cardData.cardColor.name
                    ),
                    point := self._update_start_point(point)
                )
                for line in lines
            ]

        newImage = Image.alpha_composite(image.convert("RGBA"), overlay)
        newImageDraw = ImageDraw.Draw(newImage)
        point = startPoint
        [
            (
                self._draw_text(
                    draw = newImageDraw,
                    text = line,
                    loc = point,
                    color = cardData.cardColor
                ),
                point := self._update_start_point(point)
            )
            for line in lines
        ]

        return newImage.convert("RGB")