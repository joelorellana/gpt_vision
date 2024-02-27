""" Encode the image located at the given path to base64 string. """

import base64

# Function to encode the image
def encode_image(image_path):
    """
    Encode the image located at the given path to base64 string.

    Args:
    image_path (str): The path to the image file.

    Returns:
    str: The base64 encoded string representation of the image.
    """
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')
    