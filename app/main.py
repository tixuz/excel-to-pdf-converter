from fastapi import FastAPI, UploadFile, File, Request, Form, BackgroundTasks
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import shutil
import subprocess
import os
import uuid
import logging
import asyncio

# === Logging Setup ===
LOG_PATH = "/app/pdfprinter.log"
logging.basicConfig(
    filename=LOG_PATH,
    filemode='a',
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] %(message)s'
)
logger = logging.getLogger(__name__)

# === File Size Configuration ===
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB

# === Folder Setup ===
TMP_DIR = "/app/tmp"
FONT_DIR = "/usr/share/fonts/truetype/custom"
os.makedirs(TMP_DIR, exist_ok=True)
os.makedirs(FONT_DIR, exist_ok=True)
os.chmod(TMP_DIR, 0o777)
os.chmod(FONT_DIR, 0o777)

# === Background Task Functions ===
async def delete_file_later(file_path: str, delay_minutes: int = 15):
    """
    Delete a file after a specified delay in minutes.
    Runs as a background task to clean up temporary files.
    """
    try:
        delay_seconds = delay_minutes * 60
        logger.info(f"Scheduled deletion of {file_path} in {delay_minutes} minutes")
        await asyncio.sleep(delay_seconds)

        if os.path.exists(file_path):
            os.remove(file_path)
            logger.info(f"Deleted temporary file: {file_path}")
        else:
            logger.debug(f"File already deleted: {file_path}")
    except Exception as e:
        logger.error(f"Error deleting file {file_path}: {e}")

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
async def convert_xlsx(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...)
):
    # Validate file size before processing
    file_content = await file.read()
    file_size = len(file_content)

    if file_size > MAX_FILE_SIZE:
        logger.warning(f"File too large: {file.filename} ({file_size} bytes > {MAX_FILE_SIZE} bytes)")
        return {"error": f"File too large. Maximum size is {MAX_FILE_SIZE // (1024*1024)}MB."}

    input_path = os.path.join(TMP_DIR, f"{uuid.uuid4()}.xlsx")
    output_path = input_path.replace(".xlsx", ".pdf")

    logger.info(f"Received file: {file.filename} ({file_size} bytes) → saving to {input_path}")

    try:
        # Write file to disk
        with open(input_path, "wb") as f:
            f.write(file_content)
        logger.info(f"Saved XLSX to: {input_path}")

        # Schedule cleanup for input file (even if conversion fails)
        background_tasks.add_task(delete_file_later, input_path, 15)
        logger.debug(f"Scheduled cleanup for input file: {input_path}")

        # Convert to PDF using LibreOffice
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

        # Schedule cleanup for output file
        background_tasks.add_task(delete_file_later, output_path, 15)
        logger.debug(f"Scheduled cleanup for output file: {output_path}")

        return FileResponse(
            path=output_path,
            media_type="application/pdf",
            filename=os.path.basename(output_path)
        )

    except Exception as e:
        logger.exception("Error during PDF conversion")
        return {"error": str(e)}

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
