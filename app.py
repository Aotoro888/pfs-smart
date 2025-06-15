from fastapi import FastAPI, UploadFile, Form
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import shutil

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

@app.get("/")
def read_root():
    return FileResponse("static/index.html")

@app.post("/upload")
async def upload_file(house_number: str = Form(...), month: str = Form(...), slip: UploadFile = Form(...)):
    uploads_path = Path("uploads")
    uploads_path.mkdir(exist_ok=True)
    filename = f"{house_number.replace('/', '-')}_{month}.jpg"
    save_path = uploads_path / filename
    with open(save_path, "wb") as buffer:
        shutil.copyfileobj(slip.file, buffer)
    return JSONResponse({"message": "📌 อัปโหลดสำเร็จ!"})
