from enum import Enum
from model.image import ImageAspectRatio
from PIL import Image
from typing import List

class CardType(Enum):
    STANDARD= 1
    JAPANESE= 2


DEFAULT_CARD_ASPECT_RATIOS = {
    CardType.STANDARD: ImageAspectRatio(
        width=750,
        height=1050
    ),
    CardType.JAPANESE: ImageAspectRatio(
        width=690,
        height=990
    )
}

def scale_images(images: List[Image.Image], width: int, height: int ):
    return [image.resize((width, height), resample=Image.Resampling.LANCZOS) for image in images]