from PIL import Image, ImageFont
from repository.image_repository import ImageRepository
from typing import List
from document import Document
from model.card import CardType
from model.document import DocumentType
from data.read_file import CardListFileReader
from util.text import CardText
from model.card import scale_images

LOCAL_DB: dict[str, str] = {
    "5HY/W101": "https://en.ws-tcg.com/wordpress/wp-content/images/cardimages/5HYM/W101_{}.png",
    "5HY/W83": "https://en.ws-tcg.com/wordpress/wp-content/images/cardimages/5HY/BP/5HY_W83_{}.png",
    "5HY/W83T": "https://en.ws-tcg.com/wordpress/wp-content/images/cardimages/5HY/QS/5HY_W83_{}.png",
    "5HY/WE43": "https://en.ws-tcg.com/wordpress/wp-content/images/cardimages/5HYPB/WE43_{}.png",
    "5HY/W90": "https://en.ws-tcg.com/wordpress/wp-content/images/cardimages/5HY2/W90_{}.png",
    "OVL/S99": "https://en.ws-tcg.com/wp/wp-content/images/cardimages/OVLV2/S99_{}.png",
    "OVL/S62": "https://en.ws-tcg.com/wp/wp-content/images/cardimages/o/ovl_s62/OVL_S62_{}.png",
    "SBY/W77": "https://en.ws-tcg.com/wp/wp-content/images/cardimages/SBY2/W77_{}.png",
    "SBY/W64": "https://en.ws-tcg.com/wp/wp-content/images/cardimages/s/sby_w64/SBY_W64_{}.png",
    "SBY/W114": "https://en.ws-tcg.com/wp/wp-content/images/cardimages/SBY/W114-{}.png",
    "BD/W95": "https://en.ws-tcg.com/wp/wp-content/images/cardimages/BD5TH/W95_{}.png",
    "BD/W125": "https://en.ws-tcg.com/wp/wp-content/images/cardimages/BDAM/W125_{}.png",
    "MAR/S89": "https://en.ws-tcg.com/wp/wp-content/images/cardimages/MAR/S89_{}.png",
    "GGST/SX06": "https://en.ws-tcg.com/wp/wp-content/images/cardimages/GGST/SX06_{}.png",
    "GGSTPR/SX06": "https://en.ws-tcg.com/wp/wp-content/images/cardimages/updates/PR/SX06_{}.png",
    "DAL/W79": "https://en.ws-tcg.com/wordpress/wp-content/images/cardimages/d/dal_w79/DAL_W79_{}.png",
    "DAL/W99": "https://en.ws-tcg.com/wordpress/wp-content/images/cardimages/DALv2/W99_{}.png",
    "DAL/WE33": "https://en.ws-tcg.com/wordpress/wp-content/images/cardimages/DAB/DAL_WE33_{}.png",
    "Fdl/W65": "https://en.ws-tcg.com/wordpress/wp-content/images/cardimages/f/fdi_w65/Fdl_W65_{}.png",
    "OSK/S121": "https://en.ws-tcg.com/wordpress/wp-content/images/cardimages/OSK/S121-{}.png",
    "OSK/S107": "https://en.ws-tcg.com/wordpress/wp-content/images/cardimages/OSK/S107_{}.png",
    "OVL/SE51": "https://en.ws-tcg.com/wordpress/wp-content/images/cardimages/OVL/SE51-{}.png"
}
LOCAL_JP_DB: dict[str, str] = {
    "SBY/W114", "https://ws-tcg.com/wordpress/wp-content/images/cardlist/s/sby_w114/sby_w114_{}.png"
}

def main():
    DECK_LIST_FILE = "ovl8dooreb.txt"
    OUTPUT_PDF_FILE = "ovl8dooreb.pdf"

    fr = CardListFileReader()
    # l = fr.parse_file_csv("deck.csv", "jp")
    # l = fr.parse_file_csv("dalchoicejp.csv", "jp")
    # l = fr.parse_file_local("dalchoice.txt",LOCAL_DB,"en", needExternalSource=False)
    l = fr.parse_file_comb(DECK_LIST_FILE,LOCAL_DB, needExternalSource=False)
   
    repository = ImageRepository()
    images: List[Image.Image] = repository.set_card_data(l).get_images_multiprocess()



    cardText = CardText(
    ).set_font_size(
        int(20*10/3)
    ).set_line_pading(
        int(4*10/3) #4
    ).set_spacing(
        int(8*10/3) #8
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
    for page in pages:
        print(page.size)
    # pages_reduced = scale_images(pages, int(pages[0].width/10*3), int(pages[0].height/10*3))
    # pages_reduced[0].save("daldoorjp.pdf", save_all = True, append_images = pages_reduced[1:])
    pages[0].save(OUTPUT_PDF_FILE, save_all = True, append_images = pages[1:]) 
if __name__ == "__main__":
    main()