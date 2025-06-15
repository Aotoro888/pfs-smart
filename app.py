
from fastapi import FastAPI, UploadFile, Form
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import shutil, os

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

@app.get("/")
def read_root():
    return FileResponse("static/index.html")

@app.post("/upload")
async def upload_file(house_number: str = Form(...), month: str = Form(...), payer_name: str = Form(...), slip: UploadFile = Form(...)):
    if not house_number or not month or not payer_name or not slip:
        return JSONResponse(status_code=400, content={"message": "กรุณากรอกข้อมูลให้ครบถ้วน"})

    dir_path = Path("uploads") / house_number.replace("/", "-")
    dir_path.mkdir(parents=True, exist_ok=True)
    filename = f"{month.replace(' ', '_')}_{payer_name.replace(' ', '_')}.jpg"
    file_path = dir_path / filename

    with open(file_path, "wb") as f:
        shutil.copyfileobj(slip.file, f)

    return JSONResponse({"message": "✅ อัปโหลดสำเร็จ!"})
