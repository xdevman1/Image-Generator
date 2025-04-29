from flask import Flask, render_template, request, jsonify
from g4f.client import Client
import os

app = Flask(__name__)
client = Client()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()
    prompt = data.get("prompt", "").strip()
    negative = data.get("negative", "").strip()
    aspect = data.get("aspect", "square")
    style = data.get("style", "").strip()

    
    aspect_tag = {
        "portrait": "vertical portrait",
        "landscape": "widescreen landscape",
        "square": "square"
    }.get(aspect, "")

   
    parts = [style, prompt, aspect_tag]
    final_prompt = ", ".join(filter(None, parts))  
    if negative:
        final_prompt += f", negative prompt: {negative}"

    try:
        response = client.images.generate(
            model="flux",  
            prompt=final_prompt,
            response_format="url"
        )
        return jsonify({"url": response.data[0].url})
    except Exception as e:
        print("Image generation error:", e)
        return jsonify({"error": "Image generation failed"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
