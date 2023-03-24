import logging
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import openai
from creds import api_key2
import requests

logging.basicConfig(filename='app.log',
                    filemode="a",
                    level=logging.INFO,
                    format='%(asctime)s - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S')

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def read_form(request: Request):
  return templates.TemplateResponse("index.html", {"request": request})


@app.post("/")
async def send_chatquery(request: Request,
                         prompt: str = Form(...),
                         name: str = Form(...)):
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
  return templates.TemplateResponse(
    "index.html", {
      "request": request,
      "name": name,
      "prompt": prompt,
      "response": response.choices[0].text,
    })
