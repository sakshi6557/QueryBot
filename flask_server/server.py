from flask import Flask, json, request, jsonify
import requests
import os
from groq import Groq
from dotenv import load_dotenv
from flask_cors import CORS
import re

app = Flask(__name__)
CORS(app)


def answer_question(user_question):
    load_dotenv()
    model = Groq(
        api_key=os.getenv("GROQ_API_KEY"),
    )
    system_prompt = "Your name is Querybot and you are a helpful bot who provides answer to question"
    
    message = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_question},
    ]
    chat_completion = model.chat.completions.create(
        messages=message,
        model="llama3-70b-8192",
        #stream=True,
    )
    return chat_completion.choices[0].message.content

@app.route("/chatbot", methods=["POST"])
def query():

    request_data = json.loads(request.data)
    user_question = request_data["message"]

    return jsonify({"result": answer_question(user_question)})

if __name__ == "__main__":
    app.run(debug=True)
