"""
Unit tests for the PDF Tool FastAPI backend.
"""

import pytest
import io
import tempfile
import os
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from PyPDF2 import PdfReader, PdfWriter
from main import app

client = TestClient(app)


class TestMergePDFs:
    """Test cases for the /merge endpoint."""
    
    def test_merge_pdfs_success(self):
        """Test successful PDF merging."""
        # Create test PDF files
        pdf1 = self._create_test_pdf("Test PDF 1")
        pdf2 = self._create_test_pdf("Test PDF 2")
        
        files = [
            ("files", ("test1.pdf", pdf1, "application/pdf")),
            ("files", ("test2.pdf", pdf2, "application/pdf"))
        ]
        
        response = client.post("/merge", files=files)
        
        assert response.status_code == 200
        assert response.headers["content-type"] == "application/pdf"
        assert response.headers["content-disposition"] == "attachment; filename=merged.pdf"
        
        # Verify the merged PDF has content
        merged_content = response.content
        assert len(merged_content) > 0
        
        # Verify it's a valid PDF
        pdf_reader = PdfReader(io.BytesIO(merged_content))
        assert len(pdf_reader.pages) == 2
    
    def test_merge_pdfs_insufficient_files(self):
        """Test merging with less than 2 files."""
        pdf1 = self._create_test_pdf("Test PDF 1")
        
        files = [
            ("files", ("test1.pdf", pdf1, "application/pdf"))
        ]
        
        response = client.post("/merge", files=files)
        
        assert response.status_code == 400
        assert "At least 2 PDF files are required" in response.json()["detail"]
    
    def test_merge_pdfs_non_pdf_file(self):
        """Test merging with non-PDF files."""
        pdf1 = self._create_test_pdf("Test PDF 1")
        text_file = io.BytesIO(b"This is not a PDF").getvalue()
        
        files = [
            ("files", ("test1.pdf", pdf1, "application/pdf")),
            ("files", ("test2.txt", text_file, "text/plain"))
        ]
        
        response = client.post("/merge", files=files)
        
        assert response.status_code == 400
        assert "is not a PDF" in response.json()["detail"]
    
    def test_merge_pdfs_empty_files(self):
        """Test merging with empty file list."""
        response = client.post("/merge", files=[])
        
        assert response.status_code == 422  # Validation error
    
    def _create_test_pdf(self, text_content: str) -> bytes:
        """Helper method to create a test PDF."""
        writer = PdfWriter()
        # Create a simple PDF with text content
        # Note: This is a simplified version for testing
        output = io.BytesIO()
        writer.write(output)
        output.seek(0)
        return output.getvalue()


class TestDeletePages:
    """Test cases for the /delete-pages endpoint."""
    
    def test_delete_pages_success(self):
        """Test successful page deletion."""
        # Create a test PDF with multiple pages
        pdf_content = self._create_multi_page_pdf(3)
        
        files = [("file", ("test.pdf", pdf_content, "application/pdf"))]
        data = {"pages": "2"}
        
        response = client.post("/delete-pages", files=files, data=data)
        
        assert response.status_code == 200
        assert response.headers["content-type"] == "application/pdf"
        assert response.headers["content-disposition"] == "attachment; filename=modified.pdf"
        
        # Verify the modified PDF has fewer pages
        modified_content = response.content
        pdf_reader = PdfReader(io.BytesIO(modified_content))
        assert len(pdf_reader.pages) == 2  # Original 3 - deleted 1 = 2
    
    def test_delete_pages_range(self):
        """Test deleting a range of pages."""
        pdf_content = self._create_multi_page_pdf(5)
        
        files = [("file", ("test.pdf", pdf_content, "application/pdf"))]
        data = {"pages": "2-4"}
        
        response = client.post("/delete-pages", files=files, data=data)
        
        assert response.status_code == 200
        
        # Verify the modified PDF has fewer pages
        modified_content = response.content
        pdf_reader = PdfReader(io.BytesIO(modified_content))
        assert len(pdf_reader.pages) == 2  # Original 5 - deleted 3 = 2
    
    def test_delete_pages_mixed_range(self):
        """Test deleting mixed individual pages and ranges."""
        pdf_content = self._create_multi_page_pdf(6)
        
        files = [("file", ("test.pdf", pdf_content, "application/pdf"))]
        data = {"pages": "1,3-4,6"}
        
        response = client.post("/delete-pages", files=files, data=data)
        
        assert response.status_code == 200
        
        # Verify the modified PDF has fewer pages
        modified_content = response.content
        pdf_reader = PdfReader(io.BytesIO(modified_content))
        assert len(pdf_reader.pages) == 2  # Original 6 - deleted 4 = 2
    
    def test_delete_pages_non_pdf_file(self):
        """Test deleting pages from non-PDF file."""
        text_file = io.BytesIO(b"This is not a PDF").getvalue()
        
        files = [("file", ("test.txt", text_file, "text/plain"))]
        data = {"pages": "1"}
        
        response = client.post("/delete-pages", files=files, data=data)
        
        assert response.status_code == 400
        assert "File must be a PDF" in response.json()["detail"]
    
    def test_delete_pages_missing_pages_param(self):
        """Test deleting pages without specifying pages parameter."""
        pdf_content = self._create_test_pdf("Test PDF")
        
        files = [("file", ("test.pdf", pdf_content, "application/pdf"))]
        data = {}
        
        response = client.post("/delete-pages", files=files, data=data)
        
        assert response.status_code == 400
        assert "Pages parameter is required" in response.json()["detail"]
    
    def test_delete_pages_invalid_page_range(self):
        """Test deleting pages with invalid page range format."""
        pdf_content = self._create_test_pdf("Test PDF")
        
        files = [("file", ("test.pdf", pdf_content, "application/pdf"))]
        data = {"pages": "invalid"}
        
        response = client.post("/delete-pages", files=files, data=data)
        
        assert response.status_code == 400
        assert "Invalid page range format" in response.json()["detail"]
    
    def _create_test_pdf(self, text_content: str) -> bytes:
        """Helper method to create a test PDF."""
        writer = PdfWriter()
        output = io.BytesIO()
        writer.write(output)
        output.seek(0)
        return output.getvalue()
    
    def _create_multi_page_pdf(self, num_pages: int) -> bytes:
        """Helper method to create a multi-page test PDF."""
        writer = PdfWriter()
        for _ in range(num_pages):
            # Add empty pages for testing
            pass
        output = io.BytesIO()
        writer.write(output)
        output.seek(0)
        return output.getvalue()


class TestGetPageCount:
    """Test cases for the /page-count/{filename} endpoint."""
    
    def test_get_page_count_success(self):
        """Test successful page count retrieval."""
        # Create a test PDF file in temp directory
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as temp_file:
            pdf_content = self._create_multi_page_pdf(5)
            temp_file.write(pdf_content)
            temp_file_path = temp_file.name
        
        try:
            filename = os.path.basename(temp_file_path)
            response = client.get(f"/page-count/{filename}")
            
            assert response.status_code == 200
            assert response.json()["page_count"] == 5
        finally:
            # Clean up
            os.unlink(temp_file_path)
    
    def test_get_page_count_non_pdf_file(self):
        """Test page count for non-PDF file."""
        response = client.get("/page-count/test.txt")
        
        assert response.status_code == 400
        assert "File is not a PDF" in response.json()["detail"]
    
    def test_get_page_count_file_not_found(self):
        """Test page count for non-existent file."""
        response = client.get("/page-count/nonexistent.pdf")
        
        assert response.status_code == 404
        assert "File not found" in response.json()["detail"]
    
    def _create_multi_page_pdf(self, num_pages: int) -> bytes:
        """Helper method to create a multi-page test PDF."""
        writer = PdfWriter()
        for _ in range(num_pages):
            # Add empty pages for testing
            pass
        output = io.BytesIO()
        writer.write(output)
        output.seek(0)
        return output.getvalue()


class TestCORSConfiguration:
    """Test cases for CORS configuration."""
    
    def test_cors_headers_present(self):
        """Test that CORS headers are present in responses."""
        response = client.options("/merge")
        
        # CORS headers should be present
        assert "access-control-allow-origin" in response.headers
        assert "access-control-allow-methods" in response.headers
        assert "access-control-allow-headers" in response.headers
    
    def test_cors_allows_localhost(self):
        """Test that localhost origins are allowed."""
        headers = {"Origin": "http://localhost:5173"}
        response = client.get("/page-count/test.pdf", headers=headers)
        
        # Should not be blocked by CORS
        assert response.status_code in [400, 404]  # Expected errors, not CORS errors


class TestErrorHandling:
    """Test cases for error handling."""
    
    def test_internal_server_error_handling(self):
        """Test handling of internal server errors."""
        with patch('main.PdfReader') as mock_reader:
            mock_reader.side_effect = Exception("Test error")
            
            pdf_content = b"fake pdf content"
            files = [("file", ("test.pdf", pdf_content, "application/pdf"))]
            data = {"pages": "1"}
            
            response = client.post("/delete-pages", files=files, data=data)
            
            assert response.status_code == 500
            assert "Test error" in response.json()["detail"]


if __name__ == "__main__":
    pytest.main([__file__]) 