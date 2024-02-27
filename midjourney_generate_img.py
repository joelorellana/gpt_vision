""" Generate an image using the Midjourney API"""
import io
import requests
from PIL import Image
from progress_bar import print_progress_bar
from config import GOAPIKEY

IMAGINE_ENDPOINT= "https://api.midjourneyapi.xyz/mj/v2/imagine"
FETCH_ENDPOINT = "https://api.midjourneyapi.xyz/mj/v2/fetch"

headers = {
    "X-API-KEY": GOAPIKEY
}

def midjourney_generate_img(prompt):
    """Generate an image using the Midjourney API

    Keyword arguments:
    prompt -- The prompt to generate the image from
    Return: An image saved in a .png file
    """
    img_generation_data = {
        "prompt": prompt,
        "aspect_ratio": "16:9",
        "process_mode": "fast",
        "webhook_endpoint": "",
        "webhook_secret": ""
    }
    create_img_response = requests.post(
        IMAGINE_ENDPOINT,
        headers=headers,
        json=img_generation_data,
        timeout=30)
    if create_img_response.status_code == 200:
        print("Request for an img to Midjourney: successfully!")
        task_id = create_img_response.json()['task_id']
    else:
        print(f"Image creation failed, please review details: {create_img_response.status_code} \
              {create_img_response.text}")

    print_progress_bar(50, msg='Generating MidJourney img, please wait...', bar_length=20)
    fetch_img_response = requests.post(FETCH_ENDPOINT,
                                       headers=headers,
                                       json={"task_id": task_id},
                                       timeout=30)
    status_img = fetch_img_response.json()['status']
    while status_img != "finished":
        # pause 10s
        print_progress_bar(10, msg='Generating MidJourney img, please wait...', bar_length=20)
        fetch_img_response = requests.post(FETCH_ENDPOINT,
                                           headers=headers,
                                           json={"task_id": task_id},
                                           timeout=30)
        status_img = fetch_img_response.json()['status']
        if status_img == "failed":
            print(
                f"Image generation failed, please review details: {fetch_img_response.status_code} \
                  {fetch_img_response.text}"
                  )

    # download task_result image
    print("Saving img...")
    task_result_image_url = fetch_img_response.json()['task_result']['image_url']
    image_response = requests.get(task_result_image_url, timeout=30)
    # saving img to output_img as png
    img = Image.open(io.BytesIO(image_response.content))
    img.save('output_img/midjourney_generated_img.png')
    print("Image saved in output_img/midjourney_generated_img.png")
    return "output_img/midjourney_generated_img.png"
