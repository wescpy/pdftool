"""
Pytest configuration and fixtures for backend tests.
"""

import pytest
import tempfile
import os
import shutil
from pathlib import Path


@pytest.fixture(scope="session")
def temp_dir():
    """Create a temporary directory for test files."""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)


@pytest.fixture(autouse=True)
def setup_temp_dir():
    """Ensure temp directory exists for each test."""
    temp_dir = "temp"
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    yield
    # Clean up temp files after each test
    if os.path.exists(temp_dir):
        for file in os.listdir(temp_dir):
            file_path = os.path.join(temp_dir, file)
            if os.path.isfile(file_path):
                os.unlink(file_path)


@pytest.fixture
def sample_pdf_files(temp_dir):
    """Create sample PDF files for testing."""
    from PyPDF2 import PdfWriter
    import io
    
    files = []
    
    # Create test PDF files
    for i in range(3):
        writer = PdfWriter()
        output = io.BytesIO()
        writer.write(output)
        output.seek(0)
        
        file_path = os.path.join(temp_dir, f"test{i+1}.pdf")
        with open(file_path, 'wb') as f:
            f.write(output.getvalue())
        files.append(file_path)
    
    yield files
    
    # Clean up
    for file_path in files:
        if os.path.exists(file_path):
            os.unlink(file_path)


@pytest.fixture
def multi_page_pdf(temp_dir):
    """Create a multi-page PDF file for testing."""
    from PyPDF2 import PdfWriter
    import io
    
    writer = PdfWriter()
    # Create a 5-page PDF
    for _ in range(5):
        # Add empty pages for testing
        pass
    
    output = io.BytesIO()
    writer.write(output)
    output.seek(0)
    
    file_path = os.path.join(temp_dir, "multi_page.pdf")
    with open(file_path, 'wb') as f:
        f.write(output.getvalue())
    
    yield file_path
    
    # Clean up
    if os.path.exists(file_path):
        os.unlink(file_path) 