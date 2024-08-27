import base64
import requests
from utils import client

# Function to encode the image
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

# Path to your image
image_path = "./cache/video_frames/akeytNVcIy4/frame_695.jpg"

# Getting the base64 string
base64_image = encode_image(image_path)
text_info = "You are a helpful assistant, You just need to describe the whole picture" # just the text of the things
response = client.chat.completions.create(
  model="gpt-4o-2024-08-06",
  messages=[
    {
      "role": "user",
      "content": [
        {"type": "text", "text": f"{text_info}"},
        {
          "type": "image_url",
          "image_url": {
            "url": f"data:image/jpeg;base64,{base64_image}",
          },
        },
      ],
    }
  ],
  max_tokens=300,
)

print(response.choices[0])