import base64
from io import BytesIO
from PIL import Image
import numpy as np
import os
import io

def encode(img, max_size=(320, 240)):
    """
    Encode a Pillow Image or NumPy array to base64 (JPEG).
    Automatically resizes large images to `max_size`.
    """
    if img is None:
        return None

    # Convert NumPy array to Pillow Image if needed
    if isinstance(img, np.ndarray):
        img = Image.fromarray(img)

    # Resize image if too large
    img.thumbnail(max_size)

    # Encode to JPEG bytes
    byte_stream = BytesIO()
    img.save(byte_stream, format='JPEG')
    jpeg_bytes = byte_stream.getvalue()

    # Encode to Base64
    b64_str = base64.b64encode(jpeg_bytes).decode()
    return b64_str
