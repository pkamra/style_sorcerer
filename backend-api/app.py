import json
import io
import base64
import boto3
from PIL import Image
from flask import Flask, request, jsonify
from flask_cors import CORS

from utils import bedrock, print_ww  # Assuming you have these utility functions

app = Flask(__name__)
CORS(app, supports_credentials=True)  # Enable CORS for all origins and allow credentials (cookies, HTTP authentication)

@app.route('/generate_images', methods=['POST'])
def generate_images():
    boto3_bedrock = bedrock.get_bedrock_client(region='us-east-1')

    data = request.json
    # prompt = "Witch in a Halloween dress with a pointy hat, flying broomstick, mystical setting, vibrant colors, magical aura, detailed shading, digital painting, fantasy, spooky atmosphere, popular artist influence, 4k resolution"
    prompt = data.get('prompt')

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

    # style_preset = "neon-punk"
    style_preset = data.get('style_preset', 'neon-punk')
    num_images = data.get('num_images', 5)

    uploaded_image_data_list = []
    for i in range(num_images):
        print("Sending....")
        request_send = json.dumps({
            "text_prompts": (
                [{"text": prompt}]
                + [{"text": negprompt, "weight": -1.0} for negprompt in negative_prompts]
            ),
            "cfg_scale": 9,
            "seed": i + 1,
            "steps": 100,
            "style_preset": style_preset,
        })

        modelId = "stability.stable-diffusion-xl"
        response = boto3_bedrock.invoke_model(body=request_send, modelId=modelId)
        response_body = json.loads(response.get("body").read())

        base_64_img_str = response_body["artifacts"][0].get("base64")

        # Convert base64 string to PIL Image
        image_bytes = base64.decodebytes(bytes(base_64_img_str, "utf-8"))
        pil_image = Image.open(io.BytesIO(image_bytes))

        # Convert PIL Image back to base64
        in_mem_file = io.BytesIO()
        pil_image.save(in_mem_file, format='PNG')
        in_mem_file.seek(0)
        base64_image_data = base64.b64encode(in_mem_file.read()).decode('utf-8')

        uploaded_image_data_list.append(base64_image_data)

    return jsonify({'image_data_list': uploaded_image_data_list})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
