import diplib as dip
import numpy as np
import tifffile
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
    - TIFF files are read with tifffile, so multi-frame stacks return the
      full 3D volume (callers can then extract e.g. the middle slice).
    - Other formats are read with PIL.
    """
    ext = image_path.lower()
    if ext.endswith(".ics"):
        img = load_ics_image(image_path)
    elif ext.endswith((".tif", ".tiff")):
        try:
            img = tifffile.imread(image_path)
        except Exception:
            # Some (older) TIFFs are not fully conformant; PIL is more lenient.
            img = np.array(Image.open(image_path))
    else:
        img = Image.open(image_path)

    if img is None:
        print(f"Error: Could not read image {image_path}")
        return None

    # Convert to NumPy array
    if isinstance(img, Image.Image):
        img = np.array(img)

    return img
