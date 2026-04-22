from google import genai
from google.genai import types
import base64
import os

client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])

def describe_image(base64_image: str | None) -> str:
    if not base64_image:
        return "No visual information available."
    
    # for m in client.models.list():
    #     print(m.name)

    try:
        image_bytes = base64.b64decode(base64_image)

        response = client.models.generate_content(
            model="models/gemini-2.5-flash",
            contents=[
                "Describe this image in ONE short sentence.",
                types.Part.from_bytes(
                    data=image_bytes,
                    mime_type="image/jpeg"
                )
            ],
        )

        return response.text.strip()

    except Exception as e:
        print("❌ Gemini vision error:", repr(e))
        return "Could not analyze the image."