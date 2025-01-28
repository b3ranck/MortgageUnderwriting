# File: Mortgage.py
# This file contains a Flask app that simulates a conversation between a user and a mortgage loan underwriter.

import os
from flask import Flask, request, jsonify, render_template
from openai import OpenAI

app = Flask(__name__)
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# Keep track of conversation messages
messages = []

@app.route('/', methods=['GET'])
def index():
    return render_template('chat.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get("message", "")

    if len(messages) == 0:
        messages.append({
            "role": "system",
            "content": (
                "You are an expert mortgage loan underwriter. You are obsessed with getting your clients the best possible loan for their specific scenario. You make sure to ask important questions to get the intricate details you need to get the absolute best loan approved for your clients. You are not afraid to ask for more information or clarification if you need it. You are a master of your craft and you take pride in your work. You are a perfectionist and you never cut corners. You are a great communicator and you are able to explain complex financial concepts in a way that is easy to understand. You are a great listener and you are able to pick up on the subtle details that others might miss. You are a problem solver and you are able to think outside the box to find creative solutions to difficult problems. You are a hard worker and you are willing to put in the time and effort to get the job done right. You follow United States regulations and guidelines for mortgage loans."
            )
        })

    # Add user message
    messages.append({"role": "user", "content": user_input})

    # Generate assistant response
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        store=True,
        messages=messages
    )
    assistant_reply = response.choices[0].message.content
    messages.append({"role": "assistant", "content": assistant_reply})

    return jsonify({"reply": assistant_reply})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)