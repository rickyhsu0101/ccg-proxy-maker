import requests
from PIL import Image
from typing import List, Self
from data.model.CardData import CardData
from multiprocessing import Process, Pool
from multiprocessing.pool import AsyncResult
class ImageRepository():
    def __init__(self):
        self.links: List[str] = None
        self.cardData: List[CardData] = None
    def set_image_links(self, links: List[str]):
        self.links = links
        return self
    def set_card_data(self, cardData: List[CardData]):
        self.cardData = cardData
        return self
    def _get_image(self, link) -> Image.Image | None:
        try:
           return Image.open(requests.get(link, stream=True).raw)
        except Exception as e:
            print("error on image fetch")
        return None
    def get_image(self, link: str):
        image = self._get_image(link)
        if image is None:
            return None
        imageProcessed = image.convert("RGB")
        if image is not None and image.width > image.height:
            imageProcessed = image.convert("RGB").rotate(90,expand=True) 

        return imageProcessed
    def get_images_multiprocess(self) -> List[Image.Image]:
        pool = Pool(processes=6)
        results: List[AsyncResult] = []
        if(self.links is not None):
            results = [
                pool.apply_async(self.get_image, (link,)) 
                for link in self.links
            ]
        else:
            results = [
                pool.apply_async(self.get_image, (data.url,))
                for data in self.cardData
            ]
        resImages = [res.get() for res in results]
        return [image for image in resImages if image is not None]
    def get_images(self):
        images: List[Image.Image]  = []
        if(self.links is not None):
            images= [
                self._get_image(link).convert("RGB") 
                for link in self.links
            ]
        else:
            images = [
                self._get_image(data.url).convert("RGB") 
                for data in self.cardData
            ]
        return [image.rotate(90,expand=True) if image.width > image.height else image for image in images if image is not None]