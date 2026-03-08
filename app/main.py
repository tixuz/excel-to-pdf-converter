from fastapi import FastAPI, UploadFile, File, Request, Form
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import shutil
import subprocess
import os
import uuid
import logging

# === Logging Setup ===
LOG_PATH = "/app/pdfprinter.log"
logging.basicConfig(
    filename=LOG_PATH,
    filemode='a',
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] %(message)s'
)
logger = logging.getLogger(__name__)

# === Folder Setup ===
TMP_DIR = "/app/tmp"
FONT_DIR = "/usr/share/fonts/truetype/custom"
os.makedirs(TMP_DIR, exist_ok=True)
os.makedirs(FONT_DIR, exist_ok=True)
os.chmod(TMP_DIR, 0o777)
os.chmod(FONT_DIR, 0o777)

# === App Setup ===
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# === Index Page ===
@app.get("/")
def index(request: Request):
    files = os.listdir(TMP_DIR)
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

# === Test Endpoint ===
@app.get("/hello")
def hello():
    return {"message": "Hello, world!"}

# === Upload Font ===
@app.post("/upload-font")
async def upload_font(font_file: UploadFile = File(...)):
    if not font_file.filename.endswith((".ttf", ".otf")):
        logger.warning(f"Rejected font upload: {font_file.filename}")
        return {"error": "Only .ttf and .otf fonts allowed."}

    font_path = os.path.join(FONT_DIR, font_file.filename)
    with open(font_path, "wb") as f:
        shutil.copyfileobj(font_file.file, f)

    os.system("fc-cache -fv")
    logger.info(f"Installed font: {font_file.filename}")
    return RedirectResponse(url="/", status_code=303)

# === Delete File ===
@app.post("/delete-file")
async def delete_file(filename: str = Form(...)):
    file_path = os.path.join(TMP_DIR, filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        logger.info(f"Deleted file: {file_path}")
    else:
        logger.warning(f"Tried to delete non-existent file: {file_path}")
    return RedirectResponse(url="/", status_code=303)

# === Serve Files (PDF/XLSX) ===
@app.get("/files/{filename}")
async def get_file(filename: str):
    file_path = os.path.join(TMP_DIR, filename)
    if os.path.exists(file_path):
        return FileResponse(file_path)
    logger.warning(f"Requested file not found: {file_path}")
    return {"error": "File not found"}

# === Convert XLSX to PDF ===
@app.post("/convert")
async def convert_xlsx(file: UploadFile = File(...)):
    input_path = os.path.join(TMP_DIR, f"{uuid.uuid4()}.xlsx")
    output_path = input_path.replace(".xlsx", ".pdf")

    logger.info(f"Received file: {file.filename} → saving to {input_path}")

    try:
        with open(input_path, "wb") as f:
            f.write(await file.read())
        logger.info(f"Saved XLSX to: {input_path}")

        result = subprocess.run([
            "libreoffice", "--headless", "--convert-to", "pdf", input_path, "--outdir", TMP_DIR
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
            media_type="application/pdf",
            filename=os.path.basename(output_path)
        )

    except Exception as e:
        logger.exception("Error during PDF conversion")
        return {"error": str(e)}

    # You may keep cleanup off or on:
    # finally:
    #     for path in [input_path, output_path]:
    #         if os.path.exists(path):
    #             os.remove(path)
    #             logger.debug(f"Deleted temp file: {path}")

# === PDF Management Page ===
@app.get("/pdfs")
def pdfs_page(request: Request):
    files = os.listdir(TMP_DIR)
    pdf_files = sorted([f for f in files if f.endswith('.pdf')])

    logger.info(f"Accessed PDFs page, found {len(pdf_files)} PDF files")

    return templates.TemplateResponse("pdfs.html", {
        "request": request,
        "pdf_files": pdf_files
    })

# === Font Management Page ===
@app.get("/fonts")
def fonts_page(request: Request):
    fonts_output = os.popen("fc-list : file family").readlines()
    fonts = sorted(set(line.strip() for line in fonts_output))

    logger.info(f"Accessed fonts page, found {len(fonts)} installed fonts")

    return templates.TemplateResponse("fonts.html", {
        "request": request,
        "fonts": fonts
    })

# === Queue Statistics Page ===
@app.get("/queue-stats")
def queue_stats_page(request: Request):
    # Placeholder for queue statistics
    # In a real implementation, this would connect to RabbitMQ or another queue system
    queue_len = None  # Could be replaced with actual queue length if queue system is implemented

    logger.info("Accessed queue stats page")

    return templates.TemplateResponse("queue.html", {
        "request": request,
        "queue_len": queue_len
    })
