"""
Unit tests for the PDF Tool CLI.
"""

import pytest
import tempfile
import os
import shutil
from unittest.mock import patch, MagicMock
from pathlib import Path
import sys

# Add the parent directory to the path to import pdf_tool
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pdf_tool import PDFTool


class TestPDFTool:
    """Test cases for the PDFTool class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.tool = PDFTool()
        self.temp_dir = tempfile.mkdtemp()
    
    def teardown_method(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)
        if hasattr(self.tool, 'temp_dir') and os.path.exists(self.tool.temp_dir):
            shutil.rmtree(self.tool.temp_dir, ignore_errors=True)
    
    def test_merge_pdfs_success(self):
        """Test successful PDF merging."""
        # Create test PDF files
        pdf1_path = os.path.join(self.temp_dir, "test1.pdf")
        pdf2_path = os.path.join(self.temp_dir, "test2.pdf")
        output_path = os.path.join(self.temp_dir, "merged.pdf")
        
        self._create_test_pdf(pdf1_path)
        self._create_test_pdf(pdf2_path)
        
        result = self.tool.merge_pdfs([pdf1_path, pdf2_path], output_path)
        
        assert result == output_path
        assert os.path.exists(output_path)
        assert os.path.getsize(output_path) > 0
    
    def test_merge_pdfs_insufficient_files(self):
        """Test merging with less than 2 files."""
        pdf1_path = os.path.join(self.temp_dir, "test1.pdf")
        self._create_test_pdf(pdf1_path)
        
        with pytest.raises(ValueError, match="At least 2 PDF files are required"):
            self.tool.merge_pdfs([pdf1_path])
    
    def test_merge_pdfs_file_not_found(self):
        """Test merging with non-existent files."""
        with pytest.raises(FileNotFoundError, match="File not found"):
            self.tool.merge_pdfs(["nonexistent1.pdf", "nonexistent2.pdf"])
    
    def test_merge_pdfs_non_pdf_file(self):
        """Test merging with non-PDF files."""
        pdf1_path = os.path.join(self.temp_dir, "test1.pdf")
        text_path = os.path.join(self.temp_dir, "test.txt")
        
        self._create_test_pdf(pdf1_path)
        with open(text_path, 'w') as f:
            f.write("This is not a PDF")
        
        with pytest.raises(ValueError, match="File is not a PDF"):
            self.tool.merge_pdfs([pdf1_path, text_path])
    
    def test_merge_pdfs_default_output_filename(self):
        """Test merging with default output filename."""
        pdf1_path = os.path.join(self.temp_dir, "test1.pdf")
        pdf2_path = os.path.join(self.temp_dir, "test2.pdf")
        
        self._create_test_pdf(pdf1_path)
        self._create_test_pdf(pdf2_path)
        
        # Change to temp directory to avoid conflicts
        original_cwd = os.getcwd()
        os.chdir(self.temp_dir)
        
        try:
            result = self.tool.merge_pdfs([pdf1_path, pdf2_path])
            assert result == "merged.pdf"
            assert os.path.exists("merged.pdf")
        finally:
            os.chdir(original_cwd)
    
    def test_delete_pages_success(self):
        """Test successful page deletion."""
        input_path = os.path.join(self.temp_dir, "input.pdf")
        output_path = os.path.join(self.temp_dir, "output.pdf")
        
        self._create_multi_page_pdf(input_path, 5)
        
        result = self.tool.delete_pages(input_path, "2,4", output_path)
        
        assert result == output_path
        assert os.path.exists(output_path)
        assert os.path.getsize(output_path) > 0
    
    def test_delete_pages_range(self):
        """Test deleting a range of pages."""
        input_path = os.path.join(self.temp_dir, "input.pdf")
        output_path = os.path.join(self.temp_dir, "output.pdf")
        
        self._create_multi_page_pdf(input_path, 5)
        
        result = self.tool.delete_pages(input_path, "2-4", output_path)
        
        assert result == output_path
        assert os.path.exists(output_path)
    
    def test_delete_pages_mixed_range(self):
        """Test deleting mixed individual pages and ranges."""
        input_path = os.path.join(self.temp_dir, "input.pdf")
        output_path = os.path.join(self.temp_dir, "output.pdf")
        
        self._create_multi_page_pdf(input_path, 6)
        
        result = self.tool.delete_pages(input_path, "1,3-4,6", output_path)
        
        assert result == output_path
        assert os.path.exists(output_path)
    
    def test_delete_pages_file_not_found(self):
        """Test deleting pages from non-existent file."""
        with pytest.raises(FileNotFoundError, match="File not found"):
            self.tool.delete_pages("nonexistent.pdf", "1")
    
    def test_delete_pages_non_pdf_file(self):
        """Test deleting pages from non-PDF file."""
        text_path = os.path.join(self.temp_dir, "test.txt")
        with open(text_path, 'w') as f:
            f.write("This is not a PDF")
        
        with pytest.raises(ValueError, match="File is not a PDF"):
            self.tool.delete_pages(text_path, "1")
    
    def test_delete_pages_invalid_page_numbers(self):
        """Test deleting invalid page numbers."""
        input_path = os.path.join(self.temp_dir, "input.pdf")
        output_path = os.path.join(self.temp_dir, "output.pdf")
        
        self._create_multi_page_pdf(input_path, 3)
        
        with pytest.raises(ValueError, match="Invalid page numbers"):
            self.tool.delete_pages(input_path, "5", output_path)
    
    def test_delete_pages_default_output_filename(self):
        """Test deleting pages with default output filename."""
        input_path = os.path.join(self.temp_dir, "input.pdf")
        
        self._create_multi_page_pdf(input_path, 3)
        
        # Change to temp directory to avoid conflicts
        original_cwd = os.getcwd()
        os.chdir(self.temp_dir)
        
        try:
            result = self.tool.delete_pages(input_path, "2")
            expected_output = "input_modified.pdf"
            assert result == expected_output
            assert os.path.exists(expected_output)
        finally:
            os.chdir(original_cwd)
    
    def test_get_page_count_success(self):
        """Test successful page count retrieval."""
        pdf_path = os.path.join(self.temp_dir, "test.pdf")
        self._create_multi_page_pdf(pdf_path, 7)
        
        count = self.tool.get_page_count(pdf_path)
        assert count == 7
    
    def test_get_page_count_file_not_found(self):
        """Test page count for non-existent file."""
        with pytest.raises(FileNotFoundError, match="File not found"):
            self.tool.get_page_count("nonexistent.pdf")
    
    def test_get_page_count_non_pdf_file(self):
        """Test page count for non-PDF file."""
        text_path = os.path.join(self.temp_dir, "test.txt")
        with open(text_path, 'w') as f:
            f.write("This is not a PDF")
        
        with pytest.raises(ValueError, match="File is not a PDF"):
            self.tool.get_page_count(text_path)
    
    def _create_test_pdf(self, file_path: str):
        """Helper method to create a test PDF."""
        from PyPDF2 import PdfWriter
        
        writer = PdfWriter()
        with open(file_path, 'wb') as f:
            writer.write(f)
    
    def _create_multi_page_pdf(self, file_path: str, num_pages: int):
        """Helper method to create a multi-page test PDF."""
        from PyPDF2 import PdfWriter
        
        writer = PdfWriter()
        for _ in range(num_pages):
            # Add empty pages for testing
            pass
        
        with open(file_path, 'wb') as f:
            writer.write(f)


class TestInteractiveFunctions:
    """Test cases for interactive functions."""
    
    @patch('builtins.input')
    @patch('builtins.print')
    def test_interactive_merge_success(self, mock_print, mock_input):
        """Test successful interactive merge."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create test PDF files
            pdf1_path = os.path.join(temp_dir, "test1.pdf")
            pdf2_path = os.path.join(temp_dir, "test2.pdf")
            
            from PyPDF2 import PdfWriter
            writer = PdfWriter()
            with open(pdf1_path, 'wb') as f:
                writer.write(f)
            with open(pdf2_path, 'wb') as f:
                writer.write(f)
            
            # Mock user input
            mock_input.side_effect = [pdf1_path, pdf2_path, "done", "merged.pdf"]
            
            # Import and test the function
            from pdf_tool import interactive_merge
            interactive_merge()
            
            # Verify the function was called
            assert mock_input.called
    
    @patch('builtins.input')
    @patch('builtins.print')
    def test_interactive_merge_insufficient_files(self, mock_print, mock_input):
        """Test interactive merge with insufficient files."""
        # Mock user input to add only one file then quit
        mock_input.side_effect = ["test.pdf", "done"]
        
        from pdf_tool import interactive_merge
        interactive_merge()
        
        # Verify error message was printed
        mock_print.assert_any_call("❌ At least 2 PDF files are required for merging.")
    
    @patch('builtins.input')
    @patch('builtins.print')
    def test_interactive_delete_success(self, mock_print, mock_input):
        """Test successful interactive delete."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create test PDF file
            pdf_path = os.path.join(temp_dir, "test.pdf")
            
            from PyPDF2 import PdfWriter
            writer = PdfWriter()
            with open(pdf_path, 'wb') as f:
                writer.write(f)
            
            # Mock user input
            mock_input.side_effect = [pdf_path, "2", "output.pdf"]
            
            # Import and test the function
            from pdf_tool import interactive_delete
            interactive_delete()
            
            # Verify the function was called
            assert mock_input.called


class TestErrorHandling:
    """Test cases for error handling."""
    
    def test_pdf_processing_error(self):
        """Test handling of PDF processing errors."""
        tool = PDFTool()
        
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create a corrupted PDF file
            pdf_path = os.path.join(temp_dir, "corrupted.pdf")
            with open(pdf_path, 'wb') as f:
                f.write(b"This is not a valid PDF")
            
            with pytest.raises(Exception, match="Error merging PDFs"):
                tool.merge_pdfs([pdf_path, pdf_path])
    
    def test_invalid_page_range_format(self):
        """Test handling of invalid page range format."""
        tool = PDFTool()
        
        with tempfile.TemporaryDirectory() as temp_dir:
            pdf_path = os.path.join(temp_dir, "test.pdf")
            
            from PyPDF2 import PdfWriter
            writer = PdfWriter()
            with open(pdf_path, 'wb') as f:
                writer.write(f)
            
            with pytest.raises(Exception, match="Error deleting pages"):
                tool.delete_pages(pdf_path, "invalid-range")


if __name__ == "__main__":
    pytest.main([__file__]) 