"""Generate an image using the DALL-E API

Keyword arguments:
prompt -- The prompt to generate the image from
Return: An image saved in a .png file
"""


import io
from openai import OpenAI
from PIL import Image
import requests
from config import OPENAI_API_KEY


client = OpenAI(api_key=OPENAI_API_KEY)

def generate_img_with_dalle(prompt="", ):
    """Generate an image using the DALL-E API"""
    # DALL-E model parameters
    size = '1024x1024'  # Choose between '1024x1024', '512x512', '256x256'
    quality = 'hd'  # Choose between 'standard', 'hd'
    # Generate image using DALL-E
    print('Creating DALLE image...')
    response = client.images.generate(
    model="dall-e-3",
    prompt=prompt,
    size=size,
    quality=quality,
    n=1,
    response_format="url")
    image_url = response.data[0].url
    # Download and save the image
    print('Saving image...')
    response = requests.get(image_url, timeout=30)
    img = Image.open(io.BytesIO(response.content))
    img.save('output_img/dalle_generated_img.png')  # Save the image as a .png file
    print('Image saved in output_img/dalle_generated_img.png')
    return "Image saved in output_img/dalle_generated_img.png"
