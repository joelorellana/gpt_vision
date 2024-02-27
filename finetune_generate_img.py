""" Generate an image using the Replicate API
Keyword arguments:
prompt -- The prompt to generate the image from
Return: An image saved in a .png file"""

import os
import io
import replicate
import requests
from PIL import Image
from config import REPLICATE_API_TOKEN

# Set up environment variables for Replicate API
os.environ['REPLICATE_API_TOKEN'] = REPLICATE_API_TOKEN


def generate_finetuned_img(prompt):
    """
    Generate a finetuned image based on the given prompt.

    Args:
    prompt (str): The prompt for generating the image.

    Returns:
    str: The file path of the saved finetuned image.
    """
    # Create finetuned image
    print('Creating finetuned image...')
    output = replicate.run(
    "joelorellana/paddle_modelv5:0592deeff5f62cbef89090b705196a9bc06c2874dfee85789547011dfc1f6451",
        input={
            "width": 1024,
            "height": 1024,
            "prompt": prompt,
            "refine": "base_image_refiner",
            "scheduler": "DDIM",
            "lora_scale": 0.6,
            "num_outputs": 1,
            "guidance_scale": 7.5,
            "apply_watermark": True,
            "high_noise_frac": 0.8,
            "negative_prompt": 
            """old, bad eyes, deformed, bad hands, ugly, 
               ancient, showing teeth, open mouth, two or more balls""",
            "prompt_strength": 0.8,
            "num_inference_steps": 50
        }
    )

    # Save image
    print('Saving image...')
    url = output[0]
    response = requests.get(url, timeout=30)
    img = Image.open(io.BytesIO(response.content))
    img.save('output_img/finetuned_generated_img.png')
    print('Image saved in output_img/finetuned_generated_img.png')
    return "output_img/finetuned_generated_img.png"
