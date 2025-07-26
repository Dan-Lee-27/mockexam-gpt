from flask import Flask, request, jsonify
from flask_cors import CORS
import openai

app = Flask(__name__)
CORS(app)

openai.api_key = "YOUR_OPENAI_API_KEY"  # Render에서는 환경변수로 대체됨

@app.route("/api/generate", methods=["POST"])
def generate():
    data = request.json
    topic = data.get("topic")
    q_type = data.get("question_type")
    user_id = data.get("user_id", "guest")

    prompt = f"""
You are a Korean high school English test maker.
Generate a 300–350 word passage on the topic: '{topic}'.
Then create 1 multiple-choice question ({q_type}) with 5 options (A–E).
Mark the correct answer and explain why each choice is correct or incorrect.
"""

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an expert Korean English test maker."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.75,
        max_tokens=1200
    )

    result = response["choices"][0]["message"]["content"]

    return jsonify({"result": result})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
