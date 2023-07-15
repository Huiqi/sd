from fastapi import FastAPI, Response, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import base64
import random
import string

app = FastAPI()

app.add_middleware(
    CORSMiddleware, 
    allow_credentials=True, 
    allow_origins=["*"], 
    allow_methods=["*"], 
    allow_headers=["*"]
)






#@app.get("/")
#def generate(prompt: str): 
#    with open("/total/00000a.png", 'rb') as f:
#        img_bytes = f.read()
#    imgstr = base64.b64encode(img_bytes)
#    return Response(content=imgstr, media_type="image/png")

@app.post("/")
#async def generate(code: str, param: str, image: UploadFile = File(...)):
async def generate(code: str, param: str):
    random_char = random.choice(string.ascii_lowercase[:8])
    filename = f"./api/total/{param}{random_char}.png"
    with open(filename, 'rb') as f:
        img_bytes = f.read()
    imgstr = base64.b64encode(img_bytes)
    return Response(content=imgstr, media_type="image/png")

@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}