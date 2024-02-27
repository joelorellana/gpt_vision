""" Generate a prompt for Generative AI APIs with the given image and prompt. """

import requests
from encode_image import encode_image
from config import OPENAI_API_KEY

# prompt for GPT Vision API
PROMPT = """ Return a prompt to describe the image and pass it
to DALLE or Stable Diffusion to generate an image.
The prompt must not exceed 75 tokens.
The prompt must improve the quality of the original image.
The prompt must be in the form of:
[STYLE OF PHOTO] photo of a [SUBJECT], [IMPORTANT
FEATURE], [MORE DETAILS], [POSE OR ACTION],
[FRAMING], [SETTING/BACKGROUND], [LIGHTING],
[CAMERA ANGLE], [CAMERA PROPERTIES],in style of
[PHOTOGRAPHER],
"""


def generate_prompt_with_vision(image_path, prompt=PROMPT, api_key=OPENAI_API_KEY ):
    """Generate a prompt for Generative AI APIs with the given image and prompt."""
    # Getting the base64 string
    print('Encoding image...')
    base64_image = encode_image(image_path)
    print("Encoded image. ")
    headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
    }
    payload = {
      "model": "gpt-4-vision-preview",
      "messages": [
        {
          "role": "user",
          "content": [
            {
              "type": "text",
              "text": prompt
            },
            {
              "type": "image_url",
              "image_url": {
                "url": f"data:image/jpeg;base64,{base64_image}"
              }
            }
          ]
        }
      ],
      "max_tokens": 300
    }
    print('Creating an special prompt using Vision from OpenAI...')
    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers=headers,
        json=payload,
        timeout=30)
    return response.json()['choices'][0]['message']['content']
