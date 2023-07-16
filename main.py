from fastapi import FastAPI, Response, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import base64
import random
import string
import shutil
import os
import uuid
import subprocess

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
async def generate(code: str, param: str, image: UploadFile = File(...)):
#async def generate(code: str, param: str):
    random_char = random.choice(string.ascii_lowercase[:8])
    filename = f"./api/total/{param}{random_char}.png"
    try:
        #with open(filename, 'rb') as f:
        #    img_bytes = f.read()
        #imgstr = base64.b64encode(img_bytes)
        temp_file = f"./temp/{str(uuid.uuid4())}_{image.filename}"
        output_temp_file = f"./temp/output_{str(uuid.uuid4())}_{image.filename}"
        with open(temp_file, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
        command = ["python", "./roop/run.py", "--source", temp_file, "--target", filename, "--output", output_temp_file]
        subprocess.run(command)
        if output_temp_file and os.path.exists(output_temp_file):
            with open(output_temp_file, 'rb') as f:
                img_bytes = f.read()
            imgstr = base64.b64encode(img_bytes)            
            return Response(content=imgstr, media_type="image/png")
        with open(filename, 'rb') as f:
            img_bytes = f.read()
        imgstr = base64.b64encode(img_bytes)
        
        
    finally:
        image.file.close()
        if temp_file and os.path.exists(temp_file):
            os.remove(temp_file)
        if output_temp_file and os.path.exists(output_temp_file):
            os.remove(output_temp_file)

@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}