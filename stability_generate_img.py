# pylint: disable=line-too-long
"""Generate an image using the Stability AI API

Keyword arguments:
prompt -- The prompt to generate the image from
Return: An image saved in a .png file
"""

import os
import io
import warnings

from stability_sdk import client
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation
from PIL import Image
from config import STABILITY_API_KEY

# Set up environment variables for Stability API
os.environ['STABILITY_HOST'] = 'grpc.stability.ai:443'
os.environ['STABILITY_KEY'] = STABILITY_API_KEY

# Set up our connection to the Stability API.
stability_api = client.StabilityInference(
    key=os.environ['STABILITY_KEY'],
    verbose=True,
    engine="stable-diffusion-xl-1024-v1-0",
)

def generate_image_with_stability(prompt, seed=42, steps=50, cfg_scale=7.0, width=1024, height=1024, samples=1):
    """
    Generates an image based on the given prompt using Stability API.

    :param prompt: The prompt to generate the image from.
    :param seed: Seed for deterministic generation.
    :param steps: Number of inference steps.
    :param cfg_scale: CFG scale for prompt guidance.
    :param width: Width of the generated image.
    :param height: Height of the generated image.
    :param samples: Number of images to generate.
    :return: A PIL.Image object of the generated image.
    """
    print("Creating Stability Image...")
    answers = stability_api.generate(
        prompt=prompt,
        seed=seed,
        steps=steps,
        cfg_scale=cfg_scale,
        width=width,
        height=height,
        samples=samples,
        # sampler=generation.SAMPLER_K_DPMPP_2M # default: auto
    )

    # Retrieve and process the generated image
    for resp in answers:
        for artifact in resp.artifacts:
            if artifact.finish_reason == generation.FILTER:
                warnings.warn(
                    "Your request activated the API's safety filters and could not be processed."
                    "Please modify the prompt and try again.")
            if artifact.type == generation.ARTIFACT_IMAGE:
                # saving img:
                img = Image.open(io.BytesIO(artifact.binary))
                img.save("output_img/sd_generated_img.png")
                print("Image saved in output_img/sd_generated_img.png")
                return "Image saved in output_img/sd_generated_img.png"

    raise ValueError("No image was generated.")
