FROM python:3.11-slim

# Install dependencies
RUN apt-get update && apt-get install -y \
    libreoffice \
    && apt-get clean

# Set workdir
WORKDIR /app

# Copy code
COPY app/ /app/

# Create font directory and copy fonts
COPY ./fonts /usr/share/fonts/truetype/custom/

# Rebuild font cache
RUN fc-cache -fv

# Install Python deps
RUN pip install --no-cache-dir -r requirements.txt

# Start the API
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]
