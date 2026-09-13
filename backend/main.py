import base64
from fastapi import FastAPI, File, UploadFile
import openai

app = FastAPI()
client = openai.OpenAI(api_key="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")

STREET_SMART_PROMPT = """
तू एक माहिर सोशल साइकोलॉजिस्ट और शार्प नेगोशिएटर है। 
यूजर तुझे किसी चैट का स्क्रीनशॉट देगा। 
तुझे उसे तीन सटीक हिस्सों में चीरकर रखना है:
1. असली मकसद: सामने वाला असल में क्या गेम खेल रहा है, भाव खा रहा है या क्या छुपा रहा है।
2. मनोवैज्ञानिक स्थिति: इस चैट में यूजर की क्या कमजोरी या पैनिक दिख रहा है।
3. मास्टर-स्ट्रोक रिप्लाई (3 विकल्प): 
   - (अ) दबंग और सख्त जवाब (Alpha Tone)
   - (ब) कूल और न्यूट्रल जवाब (Detached Tone)
   - (स) सामने वाले को उलझन में डालने वाला चालाक जवाब (Trap Tone).
भाषा एकदम देसी, तीखी और स्ट्रीट-स्मार्ट होनी चाहिए, कोई किताबी ज्ञान नहीं।
"""

@app.post("/decode-chat")
async def decode_chat(file: UploadFile = File(...)):
    image_bytes = await file.read()
    base64_image = base64.b64encode(image_bytes).decode('utf-8')

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": STREET_SMART_PROMPT},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "इस चैट को डिकोड कर और अपना मास्टर-स्ट्रोक दे:"},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        max_tokens=600
    )

    return {
        "status": "success",
        "analysis": response.choices[0].message.content
    }
