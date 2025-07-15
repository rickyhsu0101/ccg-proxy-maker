from PIL import Image
from repository.image_repository import ImageRepository
from typing import List
from document import Document
from model.card import CardType
from model.document import DocumentType
from data.read_file import CardListFileReader

def main():
    fr = CardListFileReader()
    l = fr.parse_file("deck.txt", "en")
    
    #return
    repository = ImageRepository()
    images: List[Image.Image] = repository.set_image_links(l).get_images_multiprocess()

    doc: Document = Document().set_dpi(1000).set_card_type(CardType.STANDARD).set_document_type(DocumentType.LETTER).set_padding(20)
    pages: List[Image.Image] = doc.output_document(images)

    pages[0].save("out3.pdf", save_all = True, append_images = pages[1:]) 
if __name__ == "__main__":
    main()