# PDF Tool - Backend API

## Quick Start

```bash
cd backend
pip install -r requirements.txt
python main.py
```

A FastAPI-based backend service for PDF manipulation operations including merging multiple PDFs and deleting pages from PDFs.

## Features

- ✅ **Merge PDFs** - Combine multiple PDF files into a single document
- ✅ **Delete Pages** - Remove specific pages or page ranges from PDFs
- ✅ **Get Page Count** - Retrieve the number of pages in a PDF file
- ✅ **CORS Support** - Configured for cross-origin requests from frontend
- ✅ **File Validation** - Ensures uploaded files are valid PDFs
- ✅ **Error Handling** - Comprehensive error responses with meaningful messages
- ✅ **Streaming Responses** - Efficient file delivery for large PDFs

## API Endpoints

### POST `/merge`
Merges multiple PDF files into a single PDF.

**Request:**
- Content-Type: `multipart/form-data`
- Body: Multiple PDF files with field name `files`

**Response:**
- Content-Type: `application/pdf`
- Body: Merged PDF file as binary data
- Headers: `Content-Disposition: attachment; filename=merged.pdf`

**Example:**
```bash
curl -X POST "http://localhost:8000/merge" \
  -H "Content-Type: multipart/form-data" \
  -F "files=@file1.pdf" \
  -F "files=@file2.pdf" \
  -F "files=@file3.pdf" \
  --output merged.pdf
```

### POST `/delete-pages`
Deletes specific pages from a PDF file.

**Request:**
- Content-Type: `multipart/form-data`
- Body: 
  - `file`: PDF file to modify
  - `pages`: Comma-separated page numbers or ranges (e.g., "1,3-5,7")

**Response:**
- Content-Type: `application/pdf`
- Body: Modified PDF file as binary data
- Headers: `Content-Disposition: attachment; filename=modified.pdf`

**Example:**
```bash
curl -X POST "http://localhost:8000/delete-pages" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@input.pdf" \
  -F "pages=1,3-5,7" \
  --output modified.pdf
```

### GET `/page-count/{filename}`
Gets the page count of a PDF file stored in the temp directory.

**Request:**
- Path parameter: `filename` - Name of the PDF file

**Response:**
```json
{
  "page_count": 10
}
```

**Example:**
```bash
curl "http://localhost:8000/page-count/document.pdf"
```

## Installation

### Prerequisites

- Python 3.8+
- pip (Python package installer)

### Setup

1. **Navigate to the backend directory:**
   ```bash
   cd backend
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the server:**
   ```bash
   python main.py
   ```

   Or using uvicorn directly:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

## Configuration

### Environment Variables

The backend can be configured using environment variables:

- `HOST` - Server host (default: `0.0.0.0`)
- `PORT` - Server port (default: `8000`)
- `CORS_ORIGINS` - Comma-separated list of allowed origins

### CORS Configuration

The backend is configured to accept requests from common frontend development ports:

```python
allow_origins=[
    "http://localhost:5173",  # Vite default
    "http://localhost:5174",  # Vite fallback
    "http://localhost:5175",  # Vite fallback
    "http://localhost:5176",  # Vite fallback
    "http://localhost:5177",  # Vite fallback
]
```

For production, update the CORS origins in `main.py` to include your frontend domain.

## Development

### Project Structure

```
backend/
├── main.py              # FastAPI application entry point
├── requirements.txt     # Python dependencies
├── temp/               # Temporary directory for file operations
└── README.md           # This file
```

### Key Components

#### `main.py`
- FastAPI application setup
- CORS middleware configuration
- API endpoint definitions
- Error handling and validation

#### Dependencies
- **FastAPI** - Modern web framework for building APIs
- **PyPDF2** - PDF manipulation library
- **uvicorn** - ASGI server for running FastAPI
- **python-multipart** - For handling file uploads

### Adding New Endpoints

To add a new endpoint, follow this pattern:

```python
@app.post("/new-endpoint")
async def new_endpoint(file: UploadFile = File(...)):
    # Validate file
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="File must be a PDF")
    
    try:
        # Process the file
        content = await file.read()
        # ... processing logic ...
        
        # Return response
        return StreamingResponse(
            output,
            media_type="application/pdf",
            headers={"Content-Disposition": "attachment; filename=result.pdf"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

## Error Handling

The backend includes comprehensive error handling:

### HTTP Status Codes

- **200 OK** - Successful operation
- **400 Bad Request** - Invalid input (wrong file type, missing parameters)
- **404 Not Found** - File not found
- **422 Unprocessable Entity** - Validation errors
- **500 Internal Server Error** - Server-side errors

### Error Response Format

```json
{
  "detail": "Error message describing the issue"
}
```

### Common Error Scenarios

1. **File not found:**
   ```json
   {"detail": "File not found: example.pdf"}
   ```

2. **Invalid file type:**
   ```json
   {"detail": "File must be a PDF"}
   ```

3. **Missing parameters:**
   ```json
   {"detail": "Pages parameter is required"}
   ```

4. **Invalid page numbers:**
   ```json
   {"detail": "Invalid page range format"}
   ```

## Testing

If you have tests implemented, run:

```bash
python -m pytest
```

If not, consider adding tests for your endpoints and PDF processing logic.

### Manual Testing

1. **Start the server:**
   ```bash
   python main.py
   ```

2. **Test merge endpoint:**
   ```bash
   curl -X POST "http://localhost:8000/merge" \
     -F "files=@test1.pdf" \
     -F "files=@test2.pdf" \
     --output merged.pdf
   ```

3. **Test delete pages endpoint:**
   ```bash
   curl -X POST "http://localhost:8000/delete-pages" \
     -F "file=@test.pdf" \
     -F "pages=1,3" \
     --output modified.pdf
   ```

### API Documentation

Once the server is running, you can access:

- **Interactive API docs:** http://localhost:8000/docs
- **ReDoc documentation:** http://localhost:8000/redoc
- **OpenAPI schema:** http://localhost:8000/openapi.json

## Deployment

### Docker Deployment

The backend includes a Dockerfile for containerized deployment:

```bash
# Build the image
docker build -t pdftool-backend .

# Run the container
docker run -p 8000:8000 pdftool-backend
```

### Google Cloud Run

The backend is configured for deployment to Google Cloud Run. See the root `cloudbuild.yaml` and `DEPLOYMENT.md` for detailed deployment instructions.

### Environment Variables for Production

Set these environment variables for production deployment:

```bash
export HOST=0.0.0.0
export PORT=8000
export CORS_ORIGINS=https://your-frontend-domain.com
```

## Security Considerations

### File Upload Security

- **File Type Validation** - Only PDF files are accepted
- **File Size Limits** - Consider implementing file size limits for production
- **Temporary Storage** - Files are processed in memory and not permanently stored

### CORS Configuration

- Configure CORS origins to only allow requests from trusted domains
- Avoid using `allow_origins=["*"]` in production

### Error Information

- Error messages are sanitized to avoid information disclosure
- Stack traces are not exposed to clients

## Performance

### Optimizations

- **Streaming Responses** - Large PDFs are streamed rather than loaded entirely into memory
- **Memory Management** - Files are processed in chunks to minimize memory usage
- **Temporary Directory** - Uses system temp directory for file operations

### Scaling Considerations

- **Stateless Design** - The service is stateless and can be horizontally scaled
- **File Processing** - PDF operations are CPU-intensive; consider resource allocation
- **Concurrent Requests** - FastAPI handles concurrent requests efficiently

## Troubleshooting

### Common Issues

1. **Port already in use:**
   ```bash
   # Kill process using port 8000
   lsof -i :8000 | grep LISTEN | awk '{print $2}' | xargs kill -9
   ```

2. **Missing dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **CORS errors from frontend:**
   - Check that the frontend URL is in the CORS origins list
   - Verify the frontend is making requests to the correct backend URL

4. **File upload errors:**
   - Ensure files are valid PDFs
   - Check file permissions
   - Verify Content-Type is `multipart/form-data`

### Logs

The server logs include:
- Request/response information
- Error details
- Processing status

Monitor logs for:
- File processing errors
- Memory usage
- Response times

## Contributing

When contributing to the backend:

1. **Follow PEP 8** - Use consistent code formatting
2. **Add Error Handling** - Ensure all endpoints have proper error handling
3. **Update Documentation** - Keep this README and API docs current
4. **Test Thoroughly** - Test with various PDF files and edge cases
5. **Consider Performance** - Monitor memory usage and processing times

## License

This backend service is part of the PDF Tool project. See the root directory for license information. 