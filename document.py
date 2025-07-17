from enum import Enum
from PIL import Image, ImageDraw
from typing import List, Tuple, Self
from model.document import *
from model.card import *
from model.layout import *
from data.model.CardData import CardData
from util.text import CardText
from math import ceil

class Document():
    def __init__(
        self, 
        docType: DocumentType = DocumentType.LETTER,
    ):
        self.docType: DocumentType = docType
        self.verticalDivider: int = 0
        self.horizontalDivider: int = 0
        self.dpi: int = 300
        self.padding: int= 0
        self.margin: int = 0
        self.cardType: CardType = CardType.STANDARD
        self.cardText = CardText()
        self.drawText: bool = False

    def set_document_type(self, docType: DocumentType):
        self.docType = docType
        return self
    
    def set_dpi(self, dpi: int):
        self.dpi = dpi
        return self
    def add_translation(self):
        self.drawText = True
        return self
    
    def set_dividers(
            self,
            vertical: int = 0,
            horizontal: int = 0
    ):
        self.verticalDivider = vertical
        self.horizontalDivider = horizontal
        return self
    def set_card_text(self, cardText: CardText):
        self.cardText = cardText
        return self
    def set_margin(
            self,
            margin: int = 0
    ):
        self.margin = margin
        return self
    
    def set_padding(
            self,
            padding: int = 0
    ):
        self.padding = padding
        return self
    
    def set_card_type(
            self,
            cardType: CardType
    ):
        self.cardType = cardType
        return self
    def _set_dim(self):
        if(self.dpi != DEFAULT_DPI):
            self.width = int(DEFAULT_DOCUMENT_DIMS[self.docType].width/DEFAULT_DOCUMENT_DIMS[self.docType].dpi*self.dpi)
            self.height = int(DEFAULT_DOCUMENT_DIMS[self.docType].height/DEFAULT_DOCUMENT_DIMS[self.docType].dpi*self.dpi)
    def _get_docinfo(self) -> DocumentInfo:
        if(self.dpi == DEFAULT_DPI):
            return DEFAULT_DOCUMENT_DIMS[self.docType]
        else:
            return DocumentInfo(
                dpi = self.dpi,
                width = self.width,
                height = self.height
            )
        
    def _determine_image_size(self, docInfo: DocumentInfo) -> Tuple[int, int]:
        width: int = DEFAULT_CARD_ASPECT_RATIOS[self.cardType].width
        height: int = DEFAULT_CARD_ASPECT_RATIOS[self.cardType].height
        if(docInfo.dpi != DEFAULT_DPI):
            return (int(width/DEFAULT_DPI*docInfo.dpi), int(height/DEFAULT_DPI*docInfo.dpi))
        return (width, height)
        
    def _compute_page_space(self) -> Tuple[int, int]:
        docInfo: DocumentInfo = self._get_docinfo()
        width = docInfo.width - 2*self.margin
        height = docInfo.height - 2*self.margin
        return width, height
    
    def _determine_layout(self, imageWidth: int, imageHeight: int) -> Tuple[int, int, int, int]:
        docInfo: DocumentInfo = self._get_docinfo()
        availableWidth, availableHeight = self._compute_page_space()
        verticalCardSpacing = max(self.verticalDivider, self.padding)
        horizontalCardSpacing = max(self.horizontalDivider, self.padding)
        #solve for x in Z
        #imageWidth * x + verticalCardSpacing * (x-1) <= availableWidth
        cardCountWidth = (availableWidth + verticalCardSpacing) // (imageWidth + verticalCardSpacing)
        cardCountHeight = (availableHeight + horizontalCardSpacing) // (imageHeight + horizontalCardSpacing)
        drawableSizeWidth = imageWidth * cardCountWidth + verticalCardSpacing * (cardCountWidth - 1)
        drawableSizeHeight = imageHeight * cardCountHeight + horizontalCardSpacing * (cardCountHeight - 1)
        startPointX = (docInfo.width-drawableSizeWidth)//2
        startPointY = (docInfo.height-drawableSizeHeight)//2
        return Layout(cardCountWidth, cardCountHeight, startPointX, startPointY)
    
    def _draw_card(self, layout: Layout, page: Image.Image, cardImage: Image.Image, cardX: int, cardY: int):
        verticalCardSpacing: int = max(self.padding, self.verticalDivider)
        horizontalCardSpacing: int = max(self.padding, self.horizontalDivider)
        drawXCoord: int = layout.startPointX + cardX * (cardImage.size[0] + verticalCardSpacing)
        drawYCoord: int = layout.startPointY + cardY * (cardImage.size[1] + horizontalCardSpacing)
        page.paste(cardImage, (drawXCoord, drawYCoord))

    def _draw_page(self, layout: Layout, page: Image.Image, pageNum: int, cardImages: List[Image.Image]):
        cardCountPerPage: int = layout.heightCount * layout.widthCount
        [
            self._draw_card(
                layout, 
                page, 
                cardImages[cardIndex], 
                (cardIndex-pageNum*cardCountPerPage)%layout.widthCount, 
                (cardIndex-pageNum*cardCountPerPage)//layout.widthCount
                )
            for cardIndex in range(pageNum*cardCountPerPage, min((pageNum+1)*cardCountPerPage, len(cardImages)))
        ]
        verticalCardSpacing: int = max(self.verticalDivider, self.padding)
        horizontalCardSpacing: int = max(self.horizontalDivider, self.padding)
        cardWidth: int = cardImages[0].width
        cardHeight: int = cardImages[0].height
        draw = ImageDraw.Draw(page)
        if(self.verticalDivider != 0):
            draw.rectangle([
                (layout.startPointX-self.verticalDivider, 0),
                (layout.startPointX, page.height-1)
            ], fill = "black", width = 0)
            [
                [
                    draw.rectangle([
                        (layout.startPointX+(layoutIndexX+1)*cardWidth + layoutIndexX*verticalCardSpacing, 0),
                        (layout.startPointX+(layoutIndexX+1)*cardWidth + layoutIndexX*verticalCardSpacing + self.verticalDivider, page.height-1)
                    ],fill="black", width=0),
                    draw.rectangle([
                        (layout.startPointX+(verticalCardSpacing-self.verticalDivider)+(layoutIndexX+1)*cardWidth + layoutIndexX*verticalCardSpacing, 0),
                        (layout.startPointX+(verticalCardSpacing-self.verticalDivider)+(layoutIndexX+1)*cardWidth + layoutIndexX*verticalCardSpacing + self.verticalDivider, page.height-1)
                    ],fill="black", width=0)
                ]
                for layoutIndexX in range(layout.widthCount - 1)
            ]
            draw.rectangle([
                (layout.startPointX+layout.widthCount*cardWidth+(layout.widthCount-1)*verticalCardSpacing, 0),
                (layout.startPointX+layout.widthCount*cardWidth+(layout.widthCount-1)*verticalCardSpacing + self.verticalDivider, page.height-1)
            ], fill = "black", width = 0)
        if(self.horizontalDivider != 0):
            draw.rectangle([
                (0, layout.startPointY - self.horizontalDivider),
                (page.width-1, layout.startPointY)
            ], fill = "black", width = 0)
            [
                [
                    draw.rectangle([
                        (0, layout.startPointY+(layoutIndexY+1)*cardHeight + layoutIndexY*horizontalCardSpacing),
                        (page.width-1, layout.startPointY+(layoutIndexY+1)*cardHeight + layoutIndexY*horizontalCardSpacing + self.horizontalDivider)
                    ],fill="black", width=0),
                    draw.rectangle([
                        (0, layout.startPointY+(horizontalCardSpacing-self.horizontalDivider)+(layoutIndexY+1)*cardHeight + layoutIndexY*horizontalCardSpacing),
                        (page.width-1, layout.startPointY+(horizontalCardSpacing-self.horizontalDivider)+(layoutIndexY+1)*cardHeight + layoutIndexY*horizontalCardSpacing + self.horizontalDivider)
                    ],fill="black", width=0)
                ]
                for layoutIndexY in range(layout.heightCount - 1)
            ]
            draw.rectangle([
                (0, layout.startPointY+layout.heightCount*cardHeight+(layout.heightCount-1)*horizontalCardSpacing),
                (page.width-1, layout.startPointY+layout.heightCount*cardHeight+(layout.heightCount-1)*horizontalCardSpacing + self.horizontalDivider)
            ], fill = "black", width = 0)

    def _draw_pages(self, cardImages: List[Image.Image], layout: Layout) -> List[Image.Image]:
        docInfo: DocumentInfo = self._get_docinfo()
        pages: int = ceil(float(len(cardImages)) / (layout.heightCount * layout.widthCount))
        pageImages: List[Image.Image] = [Image.new('RGB', (docInfo.width, docInfo.height), color = "white") for _ in range(pages)]
        [
            self._draw_page(layout, page, pageNum, cardImages)
            for pageNum, page in enumerate(pageImages)
        ]
        return pageImages
    def _draw_text(self, cardImages: List[Image.Image], cardDataList: List[CardData])-> List[Image.Image]:
        return [
            self.cardText.draw_text(cardImages[ind], cardData)
            for ind, cardData in enumerate(cardDataList)
            # if (cardData.textAnchor.compute_text_bound()) is not None
        ]
    def output_document(self, imageList: List[Image.Image], cardDataList: List[CardData] | None = None) -> List[Image.Image]:
        self._set_dim()
        print("og mode")
        # print(imageList[0].convert("RGB").mode)
        docInfo: DocumentInfo = self._get_docinfo()
        scaledWidth, scaledHeight = self._determine_image_size(docInfo)
        scaledImages: List[Image.Image] = scale_images(imageList, scaledWidth, scaledHeight)
        if(self.drawText):
            scaledImages = self._draw_text( scaledImages, cardDataList)
        layout: Layout = self._determine_layout(scaledWidth, scaledHeight)
        return self._draw_pages(scaledImages, layout)
        
