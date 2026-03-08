# GitHub Repository Setup Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Set up a professional GitHub repository for the Excel to PDF converter with comprehensive documentation and proper git configuration.

**Architecture:** Create README.md highlighting technical innovation, add .gitignore for development artifacts, clean up git staging, create repository via GitHub CLI, and push code.

**Tech Stack:** GitHub CLI (gh), git, Markdown, Python/Docker development patterns

---

### Task 1: Create comprehensive .gitignore file

**Files:**
- Create: `.gitignore`

**Step 1: Create .gitignore with Python patterns**

```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Virtual Environments
venv/
.venv/
env/
ENV/
env.bak/
venv.bak/

# IDE
.idea/
.vscode/
*.swp
*.swo
*~
.DS_Store

# System
Thumbs.db
ehthumbs.db
Desktop.ini

# Docker
*.dockerignore
docker-compose.override.yml

# Logs
*.log
logs/

# Temporary files
app/tmp/*
!app/tmp/.gitkeep

# Test files
.pytest_cache/
.coverage
htmlcov/
.tox/
```

**Step 2: Verify .gitignore syntax**

Run: `git check-ignore -v .gitignore`
Expected: No output (file shouldn't ignore itself)

**Step 3: Test with sample file**

Run: `touch test.pyc && git status --porcelain | grep test.pyc`
Expected: test.pyc appears as untracked (will be ignored when .gitignore is active)

**Step 4: Clean up test file**

Run: `rm test.pyc`

**Step 5: Commit .gitignore**

```bash
git add .gitignore
git commit -m "build: add comprehensive .gitignore for Python/Docker development"
```

---

### Task 2: Create professional README.md

**Files:**
- Create: `README.md`

**Step 1: Create README header with badges**

```markdown
# Excel to PDF Converter

![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)
![Docker](https://img.shields.io/badge/docker-✓-blue.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

> Convert Excel (.xlsx) files to PDF with a modern web interface using LibreOffice headless mode.

**Why this project matters:** Many organizations need to convert Excel reports to PDF for distribution, but existing solutions are often cumbersome or unreliable. This project provides a clean, web-based interface with industrial-strength PDF conversion via LibreOffice.
```

**Step 2: Add features section**

```markdown
## ✨ Features

- **Web-based conversion**: Upload Excel files and download PDFs through a clean web interface
- **Font management**: Upload and install custom fonts system-wide
- **Modern API**: FastAPI provides REST endpoints for automation
- **Docker containerization**: Consistent deployment across environments
- **Real-time file management**: View, download, and delete converted files
- **Comprehensive logging**: Detailed logs for debugging and monitoring
- **Security focused**: UUID-based temporary files, input validation
```

**Step 3: Add technical architecture section**

```markdown
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
```

**Step 4: Add getting started section**

```markdown
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

### Local Development
```bash
# Install Python dependencies
pip install -r app/requirements.txt

# Run the application
uvicorn app.main:app --reload --host 0.0.0.0 --port 5000

# Access at http://localhost:5000
```

### API Usage
```bash
# Convert Excel to PDF via API
curl -X POST -F "file=@report.xlsx" http://localhost:5000/convert --output output.pdf

# List installed fonts
curl http://localhost:5000/fonts
```
```

**Step 5: Add usage examples and commit**

```markdown
## 📖 Usage Examples

### Web Interface
1. Navigate to `http://localhost:5000`
2. Upload Excel file using the form
3. Download converted PDF
4. Manage files and fonts through navigation

### Font Management
1. Go to Fonts page (`/fonts`)
2. Upload `.ttf` or `.otf` files
3. Fonts become available system-wide
4. Use in Excel templates for consistent PDF output

### File Management
- View all converted PDFs on PDFs page
- Download or delete files as needed
- All operations logged to `/app/pdfprinter.log`
```

**Step 6: Add development and license sections**

```markdown
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
├── fonts/                  # Custom font files
├── Dockerfile             # Container configuration
├── README.md              # This file
└── .gitignore            # Git ignore patterns
```

### Running Tests
```bash
# Install test dependencies
pip install pytest

# Run tests
pytest
```

### Contributing
1. Fork the repository
2. Create a feature branch
3. Make changes with tests
4. Submit a pull request

## 📄 License
MIT License - see LICENSE file for details
```

**Step 7: Commit README.md**

```bash
git add README.md
git commit -m "docs: add comprehensive README with features, usage, and architecture"
```

---

### Task 3: Clean up git staging area

**Files:**
- Modify: Git staging (remove unwanted files)

**Step 1: Check current git status**

Run: `git status`
Expected: See staged and unstaged changes

**Step 2: Remove IDE files from staging**

```bash
git reset .idea/
git reset app/__pycache__/
```

**Step 3: Remove log file from staging**

```bash
git reset app/pdfprinter.log
```

**Step 4: Add .gitkeep to tmp directory**

```bash
touch app/tmp/.gitkeep
git add app/tmp/.gitkeep
```

**Step 5: Stage all good changes**

```bash
git add app/
git add fonts/
git add Dockerfile
git add CLAUDE.md
git add docs/
```

**Step 6: Verify clean staging**

Run: `git status --porcelain`
Expected: Only desired files in staging

**Step 7: Commit cleaned state**

```bash
git commit -m "chore: clean up staging, add .gitkeep for tmp directory"
```

---

### Task 4: Create GitHub repository

**Files:**
- Remote: Create GitHub repository via CLI

**Step 1: Check GitHub CLI authentication**

Run: `gh auth status`
Expected: Logged in to github.com

**Step 2: Create repository**

```bash
gh repo create excel-to-pdf-converter --public --description "Convert Excel files to PDF with a modern web interface using LibreOffice" --source=. --remote=origin --push
```

**Step 3: Verify repository creation**

Run: `gh repo view`
Expected: Repository details displayed

**Step 4: Verify remote configuration**

Run: `git remote -v`
Expected: Shows origin pointing to new repository

**Step 5: Push all branches**

```bash
git push --all origin
```

**Step 6: Verify push succeeded**

Run: `git log --oneline -3`
Expected: Recent commits shown

---

### Task 5: Final verification

**Files:**
- Remote: GitHub repository

**Step 1: Check repository URL**

Run: `gh repo view --web`
Expected: Browser opens to repository page

**Step 2: Verify README renders**

Manual: Check GitHub page shows formatted README

**Step 3: Verify .gitignore works**

Run: `git status --porcelain`
Expected: No unwanted files tracked

**Step 4: Create initial tag**

```bash
git tag v0.1.0
git push origin v0.1.0
```

**Step 5: Final status check**

Run: `git status && git log --oneline -5`
Expected: Clean working tree with recent commits

---

## Post-Implementation Checklist

- [ ] Repository accessible at `github.com/[username]/excel-to-pdf-converter`
- [ ] README.md renders correctly with all sections
- [ ] .gitignore excludes development artifacts
- [ ] No sensitive data committed
- [ ] Docker build works from repository
- [ ] Web interface accessible after deployment