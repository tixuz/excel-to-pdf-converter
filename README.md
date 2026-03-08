 # Excel to PDF Converter

![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)
![Docker](https://img.shields.io/badge/docker-✓-blue.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

> Convert Excel (.xlsx) files to PDF with a modern web interface using LibreOffice headless mode.

**Why this project matters:** Many organizations need to convert Excel reports to PDF for distribution, but existing solutions are often cumbersome or unreliable. This project provides a clean, web-based interface with industrial-strength PDF conversion via LibreOffice.

## ✨ Features

- **Web-based conversion**: Upload Excel files and download PDFs through a clean web interface
- **Font management**: Upload and install custom fonts system-wide
- **Modern API**: FastAPI provides REST endpoints for automation
- **Docker containerization**: Consistent deployment across environments
- **Real-time file management**: View, download, and delete converted files
- **Comprehensive logging**: Detailed logs for debugging and monitoring
- **Security focused**: UUID-based temporary files, input validation

## 🏗️ Technical Architecture

This project demonstrates several interesting technical approaches:

### Core Components
- **FastAPI Application**: Async Python web framework for high-performance endpoints
- **LibreOffice Headless**: Industrial-strength PDF conversion without GUI dependencies
- **Fontconfig Integration**: System-wide font management with `fc-cache`
- **Jinja2 Templates**: Dynamic web interface with DataTables for file listings
- **Docker Containerization**: Isolated, reproducible deployment environment

### Conversion Pipeline
1. Excel file uploaded via web interface or API
2. Saved with UUID filename to prevent path traversal
3. LibreOffice runs `--headless --convert-to pdf`
4. Generated PDF served for download
5. Optional temporary file cleanup

### Security Features
- File type validation (.xlsx, .ttf, .otf only)
- UUID-based temporary filenames
- Exact filename matching for deletions
- Subprocess isolation for LibreOffice

## 🚀 Getting Started

### Prerequisites
- Python 3.11+ or Docker
- Git

### Quick Start with Docker
```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/excel-to-pdf-converter.git
cd excel-to-pdf-converter

# Build and run
docker build -t excel-to-pdf .
docker run -p 5000:5000 excel-to-pdf

# Access the web interface at http://localhost:5000
```

**Note**: Replace `YOUR_USERNAME` with your actual GitHub username or fork the repository first.

### Local Development
```bash
# Install Python dependencies
pip install -r app/requirements.txt

# Run the application
uvicorn app.main:app --reload --host 0.0.0.0 --port 5000

# Access at http://localhost:5000
```

### API Usage

The application provides RESTful API endpoints for programmatic access. FastAPI automatically generates interactive API documentation at `http://localhost:5000/docs`.

**Core API Endpoints:**

```bash
# Convert Excel to PDF
curl -X POST -F "file=@report.xlsx" http://localhost:5000/convert --output output.pdf

# Upload custom fonts (.ttf or .otf)
curl -X POST -F "font_file=@custom-font.ttf" http://localhost:5000/upload-font

# Download files (PDF/XLSX)
curl http://localhost:5000/files/filename.pdf --output downloaded.pdf

# Delete files
curl -X POST -d "filename=file-to-delete.pdf" http://localhost:5000/delete-file

# Test endpoint
curl http://localhost:5000/hello
```

**Web Interface Endpoints:**
- `GET /` - Main dashboard with file management
- `GET /pdfs` - PDF file listings
- `GET /fonts` - Font management interface (Note: This is a web page, not a JSON API endpoint)
- `GET /queue-stats` - Queue statistics interface

## 📖 Usage Examples

### Web Interface
1. Navigate to `http://localhost:5000`
2. Upload Excel file using the form
3. Download converted PDF
4. Manage files and fonts through navigation

### Font Management
1. Go to Fonts page (`/fonts`) in the web interface
2. Upload `.ttf` or `.otf` files through the web form or API
3. Fonts become available system-wide after `fc-cache` refresh
4. Use in Excel templates for consistent PDF output

### File Management
- View all converted PDFs on PDFs page
- Download or delete files as needed
- All operations logged to `/app/pdfprinter.log`

## 🛠️ Development

### Project Structure
```
excel-to-pdf-converter/
├── app/
│   ├── main.py              # FastAPI application
│   ├── requirements.txt     # Python dependencies
│   ├── static/             # CSS and static assets
│   ├── templates/          # Jinja2 HTML templates
│   └── tmp/                # Temporary file storage
├── docs/                   # Documentation and planning
│   └── plans/             # Project planning documents
├── fonts/                  # Custom font files
├── Dockerfile             # Container configuration
├── README.md              # This file
└── .gitignore            # Git ignore patterns
```

### Testing

**Interactive Testing:**
- Access the FastAPI auto-generated documentation at `http://localhost:5000/docs`
- Test API endpoints directly from the browser
- View request/response schemas and examples

**Manual Testing:**
- Upload Excel files through the web interface
- Verify PDF conversion quality
- Test font upload and system-wide availability
- Check file download and deletion functionality

**Note:** Comprehensive automated test suite is planned for future development.

### Contributing
1. Fork the repository
2. Create a feature branch
3. Make changes with tests
4. Submit a pull request

## 📄 License
MIT License - see LICENSE file for details