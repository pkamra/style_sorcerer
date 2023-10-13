import json
import io
import base64
import os
import sys
import boto3
from PIL import Image
from flask import Flask, request, jsonify

from utils import bedrock, print_ww

app = Flask(__name__)

@app.route('/generate_images', methods=['POST'])
def generate_images():
    boto3_bedrock = bedrock.get_bedrock_client(region='us-east-1')

    data = request.json
    # prompt = data.get('prompt')
    prompt = "Witch in a Halloween dress with a pointy hat, flying broomstick, mystical setting, vibrant colors, magical aura, detailed shading, digital painting, fantasy, spooky atmosphere, popular artist influence, 4k resolution"

    # negative_prompts = data.get('negative_prompts', [])
    negative_prompts = [
    "malformed limbs",
    "extra limbs",
    "Dull and unappealing designs", 
    "low-quality stitching", 
    "faded colors", 
    "poorly crafted gold earrings", 
    "lack of cultural authenticity", 
    "blurry and pixelated images", 
    "low-resolution visuals",
    "people"
    ]

    # style_preset = data.get('style_preset', 'neon-punk')
    style_preset = "neon-punk"
    num_images = data.get('num_images', 5)

    # Your existing code for generating images goes here
    # ...

    # Upload images to S3
    s3 = boto3.client('s3')
    uploaded_image_urls = []
    for i in range(num_images):
        request_send = json.dumps({
            "text_prompts": (
                [{"text": prompt}]
                + [{"text": negprompt, "weight": -1.0} for negprompt in negative_prompts]
            ),
            "cfg_scale": 9,
            "seed": i + 1,  # Change seed for each iteration to get different images
            "steps": 100,
            "style_preset": style_preset,
        })

        modelId = "stability.stable-diffusion-xl"
        response = boto3_bedrock.invoke_model(body=request_send, modelId=modelId)
        response_body = json.loads(response.get("body").read())

        print(response_body["result"])
        base_64_img_str = response_body["artifacts"][0].get("base64")
        print(f"{base_64_img_str[0:80]}...")

        # Convert base64 string to PIL Image
        image_bytes = base64.decodebytes(bytes(base_64_img_str, "utf-8"))
        pil_image = Image.open(io.BytesIO(image_bytes))

        # Save the image to an in-memory file
        in_mem_file = io.BytesIO()
        pil_image.save(in_mem_file, format='PNG')
        in_mem_file.seek(0)

        # Upload image to S3
        bucket_name = 'stable-diffusion-12826'
        key = f'apiimage_{i + 1}.png'
        s3.upload_fileobj(in_mem_file, bucket_name, key)

        # Get the public URL of the uploaded image
        image_url = f'https://{bucket_name}.s3.amazonaws.com/{key}'
        uploaded_image_urls.append(image_url)

    return jsonify({'image_urls': uploaded_image_urls})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
