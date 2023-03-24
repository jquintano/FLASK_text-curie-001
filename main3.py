import logging
from flask import Flask, render_template, request, session
from flask_session import Session
import openai
import uuid
from creds import api_key2

logging.basicConfig(
    filename='app.log',
    filemode="a",
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%d-%b-%y %H:%M:%S'
)

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
app.secret_key = api_key2
Session(app)

@app.route("/")
def index():
    if 'user_id' not in session:
        session['user_id'] = str(uuid.uuid4())
        logging.info(f"New visitor with ID {session['user_id']} accessed the site")

    return render_template("index.html")

@app.route("/", methods=["POST"])
def send_chatquery():
    prompt = request.form.get('prompt')
    name = request.form.get('name')
    logging.info(f"{session['user_id']} : {name} asked: {prompt}")
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
##    app.run(debug=True)
    app.run()
