from fastapi import FastAPI, UploadFile, File, Request, Form
from fastapi.responses import FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import shutil
import subprocess
import os
import uuid



app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
import logging

LOG_PATH = "/app/pdfprinter.log"
logging.basicConfig(
    filename=LOG_PATH,
    filemode='a',
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] %(message)s'
)

logger = logging.getLogger(__name__)

TMP_DIR = "/app/tmp"
os.makedirs(TMP_DIR, exist_ok=True)
os.chmod(TMP_DIR, 0o777)

app = FastAPI()

@app.get("/")
def index(request: Request):
    files = os.listdir("/app/tmp")
    xlsx_files = sorted([f for f in files if f.endswith('.xlsx')])
    pdf_files = sorted([f for f in files if f.endswith('.pdf')])

    fonts_output = os.popen("fc-list : file family").readlines()
    fonts = sorted(set(line.strip() for line in fonts_output))

    return templates.TemplateResponse("index.html", {
        "request": request,
        "xlsx_files": xlsx_files,
        "pdf_files": pdf_files,
        "fonts": fonts
    })

@app.get("/hello")
def hello():
    return {"message": "Hello, world!"}

@app.post("/upload-font")
async def upload_font(font_file: UploadFile = File(...)):
    if not font_file.filename.endswith((".ttf", ".otf")):
        return {"error": "Only .ttf and .otf fonts allowed."}

    font_path = f"/usr/share/fonts/truetype/custom/{font_file.filename}"
    with open(font_path, "wb") as f:
        shutil.copyfileobj(font_file.file, f)

    os.system("fc-cache -fv")
    return RedirectResponse(url="/", status_code=303)

@app.post("/delete-file")
async def delete_file(filename: str = Form(...)):
    file_path = os.path.join("/app/tmp", filename)
    if os.path.exists(file_path):
        os.remove(file_path)
    return RedirectResponse(url="/", status_code=303)

@app.get("/files/{filename}")
async def get_file(filename: str):
    file_path = os.path.join("/app/tmp", filename)
    if os.path.exists(file_path):
        return FileResponse(file_path)
    return {"error": "File not found"}


@app.post("/convert")
async def convert_xlsx(file: UploadFile = File(...)):
    input_path = f"{TMP_DIR}/{uuid.uuid4()}.xlsx"
    output_path = input_path.replace('.xlsx', '.pdf')
    logger.info(f"Received file: {file.filename} → saving to {input_path}")

    try:
        with open(input_path, 'wb') as f:
            f.write(await file.read())
        logger.info(f"Saved file to: {input_path}")

        result = subprocess.run([
            "libreoffice",
            "--headless",
            "--convert-to", "pdf",
            input_path,
            "--outdir", TMP_DIR
        ], capture_output=True, text=True)

        if result.returncode != 0:
            logger.error(f"LibreOffice failed: {result.stderr}")
            return {"error": result.stderr}
        else:
            if result.stderr:
                logger.warning(f"LibreOffice warnings: {result.stderr}")

        logger.info(f"PDF created at: {output_path}")
        return FileResponse(
            path=output_path,
            media_type='application/pdf',
            filename=os.path.basename(output_path)
        )

    except Exception as e:
        logger.exception("Error during PDF conversion")
        return {"error": str(e)}

#     finally:
#         for path in [input_path, output_path]:
#             if os.path.exists(path):
#                 os.remove(path)
#                 logger.debug(f"Deleted temp file: {path}")
