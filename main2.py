import logging
from flask import Flask, render_template, request
import openai
from creds import api_key2

logging.basicConfig(
    filename='app.log',
    filemode="a",
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%d-%b-%y %H:%M:%S'
)

app = Flask(__name__, static_folder='static')

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/", methods=["POST"])
def send_chatquery():
    prompt = request.form.get('prompt')
    name = request.form.get('name')
    logging.info(f"{name} asked: {prompt}")
    openai.api_key = api_key2
    model = "text-davinci-002"
    response = openai.Completion.create(
        engine=model,
        prompt=prompt,
        max_tokens=900,
        n=1,
        stop=None,
        temperature=0.7,
    )
    return render_template(
        "index.html",
        name=name,
        prompt=prompt,
        response=response.choices[0].text
    )

if __name__ == "__main__":
##    app.run(host='0.0.0.0', port=8080)
    app.run(debug=True)
