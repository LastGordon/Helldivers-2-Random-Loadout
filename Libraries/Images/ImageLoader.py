import os
from PIL import Image

class ImageLoader:
    def __init__(self, base_path):
        self.base_path = base_path

    def load_images(self, category, image_name):
        """
        Loads an image from the specified category folder.
        :param category: Folder category (e.g., 'Eagle', 'Orbital', 'Sentry', etc.)
        :param image_name: Name of the image file (e.g., 'Helldiver.png')
        :return: Loaded image using PIL.Image
        """
        image_path = os.path.join(self.base_path, category, image_name)
        try:
            img = Image.open(image_path)
            return img
        except FileNotFoundError:
            print(f"Image {image_name} not found in {category}.")
            return None
        
    def load_generic_helldiver_image(self):
        """
        Loads the generic Helldiver image.
        :return: Loaded image of Helldiver
        """
        return self.load_images("", "Helldiver.png")