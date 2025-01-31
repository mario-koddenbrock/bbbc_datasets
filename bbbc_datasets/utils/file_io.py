import diplib as dip
import numpy as np
from PIL import Image


def load_ics_image(image_path):
    """
    Reads an ICS image and returns it as a NumPy array.
    """
    img = dip.ImageRead(image_path)
    return np.array(img)


def load_image(image_path):
    """
    Loads an image (2D or 3D) and converts it to a displayable format.
    - If the image is 3D (e.g., TIFF stack), it extracts the middle slice.
    - If the image is grayscale, it normalizes it for display.
    """
    if image_path.endswith(".ics") or image_path.endswith(".tiff"):
        img = load_ics_image(image_path)
    else:
        img = Image.open(image_path)

    if img is None:
        print(f"Error: Could not read image {image_path}")
        return None

    # Convert to NumPy array
    if isinstance(img, Image.Image):
        img = np.array(img)

    return img
