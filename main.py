from PIL import Image, ImageFont
from repository.image_repository import ImageRepository
from typing import List
from document import Document
from model.card import CardType
from model.document import DocumentType
from data.read_file import CardListFileReader
from util.text import CardText


# LOCAL_DB: dict[str, str] = {
#     MKI/W126
# }

def main():
    # def formatter(series, sets, id):
    #     return f"https://en.ws-tcg.com/wp/wp-content/images/cardimages/n/{series.lower()}_{sets.lower()}/{series.upper()}_{sets.upper()}_{id.upper()}.png"
    
    fr = CardListFileReader()
    #l = fr.parse_file_csv("deck.csv", "jp")
    l = fr.parse_file_csv("deck2.csv", "jp")
    # l = fr.parse_file_local("deck.txt",formatter,"en")
    #print(l)
    #return
    repository = ImageRepository()
    # images: List[Image.Image] = repository.set_image_links(l).get_images_multiprocess()
    images: List[Image.Image] = repository.set_card_data(l).get_images_multiprocess()

    cardText = CardText(
    ).set_font_size(
        int(20*10/3)
    ).set_line_pading(
        int(4*10/3)
    ).set_spacing(
        int(8*10/3)
    ).set_outline_rect(
        True
    ).set_full_background(
        True
    ).set_stroke_width(3) #2*10/3 #int(3)

    doc: Document = Document().set_dpi(
        1000
    ).set_card_text(
        cardText
    ).add_translation(
    ).set_card_type(
        CardType.STANDARD
    ).set_document_type(
        DocumentType.LETTER
    ).set_padding(
        30
    ).set_dividers(10,10)
    # doc: Document = Document().set_dpi(1000).set_card_type(CardType.STANDARD).set_document_type(DocumentType.LETTER).set_padding(30).set_dividers(10,10)
    pages: List[Image.Image] = doc.output_document(imageList= images, cardDataList=l)

    pages[0].save("mkichoicebar8.pdf", save_all = True, append_images = pages[1:]) 
if __name__ == "__main__":
    main()