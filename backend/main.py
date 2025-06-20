from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from PyPDF2 import PdfReader, PdfWriter
import os
import shutil
from typing import List
import tempfile
import io
import re

app = FastAPI(title="PDFtool API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174", "http://localhost:5175", "http://localhost:5176", "http://localhost:5177"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create temporary directory for file operations
TEMP_DIR = "temp"
if not os.path.exists(TEMP_DIR):
    os.makedirs(TEMP_DIR)

@app.post("/merge")
async def merge_pdfs(files: List[UploadFile] = File(...)):
    if len(files) < 2:
        raise HTTPException(status_code=400, detail="At least 2 PDF files are required")
    merger = PdfWriter()
    try:
        for file in files:
            if not file.filename.lower().endswith('.pdf'):
                raise HTTPException(status_code=400, detail=f"File {file.filename} is not a PDF")
            content = await file.read()
            pdf = PdfReader(io.BytesIO(content))
            for page in pdf.pages:
                merger.add_page(page)
        output = io.BytesIO()
        merger.write(output)
        output.seek(0)
        return StreamingResponse(
            output,
            media_type="application/pdf",
            headers={"Content-Disposition": "attachment; filename=merged.pdf"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/delete-pages")
async def delete_pages(file: UploadFile = File(...), pages: str = Form(...)):
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="File must be a PDF")
    if not pages:
        raise HTTPException(status_code=400, detail="Pages parameter is required")
    try:
        page_numbers = set()
        for part in pages.split(','):
            part = part.strip()
            if '-' in part:
                start, end = map(int, part.split('-'))
                page_numbers.update(range(start, end + 1))
            else:
                page_numbers.add(int(part))
        content = await file.read()
        pdf = PdfReader(io.BytesIO(content))
        writer = PdfWriter()
        for i in range(len(pdf.pages)):
            if i + 1 not in page_numbers:
                writer.add_page(pdf.pages[i])
        output = io.BytesIO()
        writer.write(output)
        output.seek(0)
        return StreamingResponse(
            output,
            media_type="application/pdf",
            headers={"Content-Disposition": "attachment; filename=modified.pdf"}
        )
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid page range format")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/page-count/{filename}")
async def get_page_count(filename: str):
    if not filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="File is not a PDF")
    file_path = os.path.join(TEMP_DIR, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    reader = PdfReader(file_path)
    return {"page_count": len(reader.pages)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 