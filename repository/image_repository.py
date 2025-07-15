import requests
from PIL import Image
from typing import List
from multiprocessing import Process, Pool
class ImageRepository():
    def __init__(self):
        self.links: List[str] = []
    def set_image_links(self, links: List[str]):
        self.links = links
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
        return image.convert("RGB").rotate(90,expand=True) if image is not None and image.width > image.height else image
    def get_images_multiprocess(self):
        pool = Pool(processes=6)
        results = [pool.apply_async(self.get_image, (link,)) for link in self.links]
        resImages = [res.get() for res in results]
        return [image for image in resImages if image is not None]
    def get_images(self):
        images: List[Image.Image] = [self._get_image(link).convert("RGB") for link in self.links]
        return [image.rotate(90,expand=True) if image.width > image.height else image for image in images if image is not None]