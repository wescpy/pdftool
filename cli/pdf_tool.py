#!/usr/bin/env python3
"""
PDF Tool - Command Line Interface
A simple command-line tool for merging PDFs and deleting pages from PDFs.
"""

import argparse
import os
import sys
from pathlib import Path
from typing import List
from PyPDF2 import PdfReader, PdfWriter
import tempfile


class PDFTool:
    def __init__(self):
        self.temp_dir = tempfile.mkdtemp()

    def merge_pdfs(self, input_files: List[str], output_file: str = None) -> str:
        """
        Merge multiple PDF files into a single PDF.
        
        Args:
            input_files: List of input PDF file paths
            output_file: Output PDF file path (optional)
            
        Returns:
            Path to the merged PDF file
        """
        if len(input_files) < 2:
            raise ValueError("At least 2 PDF files are required for merging")
        
        # Validate input files
        for file_path in input_files:
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"File not found: {file_path}")
            if not file_path.lower().endswith('.pdf'):
                raise ValueError(f"File is not a PDF: {file_path}")
        
        # Generate output filename if not provided
        if output_file is None:
            output_file = "merged.pdf"
        
        merger = PdfWriter()
        
        try:
            print(f"Processing {len(input_files)} PDF files...")
            
            for i, file_path in enumerate(input_files, 1):
                print(f"  [{i}/{len(input_files)}] Reading: {os.path.basename(file_path)}")
                
                with open(file_path, 'rb') as file:
                    pdf = PdfReader(file)
                    for page in pdf.pages:
                        merger.add_page(page)
            
            # Write merged PDF
            print(f"Writing merged PDF to: {output_file}")
            with open(output_file, 'wb') as output:
                merger.write(output)
            
            print(f"✅ Successfully merged {len(input_files)} PDFs into: {output_file}")
            return output_file
            
        except Exception as e:
            raise Exception(f"Error merging PDFs: {str(e)}")

    def delete_pages(self, input_file: str, pages_to_delete: str, output_file: str = None) -> str:
        """
        Delete specific pages from a PDF file.
        
        Args:
            input_file: Input PDF file path
            pages_to_delete: Comma-separated page numbers or ranges (e.g., "1,3-5,7")
            output_file: Output PDF file path (optional)
            
        Returns:
            Path to the modified PDF file
        """
        if not os.path.exists(input_file):
            raise FileNotFoundError(f"File not found: {input_file}")
        
        if not input_file.lower().endswith('.pdf'):
            raise ValueError(f"File is not a PDF: {input_file}")
        
        # Generate output filename if not provided
        if output_file is None:
            base_name = os.path.splitext(input_file)[0]
            output_file = f"{base_name}_modified.pdf"
        
        try:
            # Parse page ranges
            page_numbers = set()
            for part in pages_to_delete.split(','):
                part = part.strip()
                if '-' in part:
                    start, end = map(int, part.split('-'))
                    page_numbers.update(range(start, end + 1))
                else:
                    page_numbers.add(int(part))
            
            print(f"Reading PDF: {input_file}")
            
            # Keep the file open while processing
            with open(input_file, 'rb') as file:
                pdf = PdfReader(file)
                total_pages = len(pdf.pages)
                
                print(f"Total pages in PDF: {total_pages}")
                print(f"Pages to delete: {sorted(page_numbers)}")
                
                # Validate page numbers
                invalid_pages = [p for p in page_numbers if p < 1 or p > total_pages]
                if invalid_pages:
                    raise ValueError(f"Invalid page numbers: {invalid_pages}. Pages must be between 1 and {total_pages}")
                
                writer = PdfWriter()
                
                # Add all pages except those in page_numbers
                pages_kept = 0
                for i in range(total_pages):
                    if i + 1 not in page_numbers:  # +1 because pages are 1-indexed
                        writer.add_page(pdf.pages[i])
                        pages_kept += 1
                
                # Write modified PDF
                print(f"Writing modified PDF to: {output_file}")
                with open(output_file, 'wb') as output:
                    writer.write(output)
            
            print(f"✅ Successfully deleted {len(page_numbers)} pages. Kept {pages_kept} pages.")
            print(f"Output saved to: {output_file}")
            return output_file
            
        except Exception as e:
            raise Exception(f"Error deleting pages: {str(e)}")

    def get_page_count(self, file_path: str) -> int:
        """Get the number of pages in a PDF file."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        if not file_path.lower().endswith('.pdf'):
            raise ValueError(f"File is not a PDF: {file_path}")
        
        with open(file_path, 'rb') as file:
            pdf = PdfReader(file)
            return len(pdf.pages)


def interactive_merge():
    """Interactive mode for merging PDFs."""
    print("\n=== PDF Merge Tool ===")
    
    pdf_files = []
    while True:
        file_path = input("\nEnter PDF file path (or 'done' to finish): ").strip()
        
        if file_path.lower() == 'done':
            break
        
        if not file_path:
            print("Please enter a valid file path.")
            continue
        
        if not os.path.exists(file_path):
            print(f"❌ File not found: {file_path}")
            continue
        
        if not file_path.lower().endswith('.pdf'):
            print(f"❌ File is not a PDF: {file_path}")
            continue
        
        pdf_files.append(file_path)
        print(f"✅ Added: {file_path}")
    
    if len(pdf_files) < 2:
        print("❌ At least 2 PDF files are required for merging.")
        return
    
    output_file = input("\nEnter output filename (default: merged.pdf): ").strip()
    if not output_file:
        output_file = "merged.pdf"
    
    try:
        tool = PDFTool()
        tool.merge_pdfs(pdf_files, output_file)
    except Exception as e:
        print(f"❌ Error: {e}")


def interactive_delete():
    """Interactive mode for deleting pages."""
    print("\n=== PDF Page Deletion Tool ===")
    
    while True:
        file_path = input("\nEnter PDF file path: ").strip()
        
        if not file_path:
            print("Please enter a valid file path.")
            continue
        
        if not os.path.exists(file_path):
            print(f"❌ File not found: {file_path}")
            continue
        
        if not file_path.lower().endswith('.pdf'):
            print(f"❌ File is not a PDF: {file_path}")
            continue
        
        break
    
    try:
        tool = PDFTool()
        page_count = tool.get_page_count(file_path)
        print(f"\n📄 Total pages in PDF: {page_count}")
        print("Page numbers range from 1 to", page_count)
        
        while True:
            pages_input = input("\nEnter pages to delete (e.g., 1,3-5,7): ").strip()
            
            if not pages_input:
                print("Please enter page numbers.")
                continue
            
            try:
                # Validate page numbers
                page_numbers = set()
                for part in pages_input.split(','):
                    part = part.strip()
                    if '-' in part:
                        start, end = map(int, part.split('-'))
                        page_numbers.update(range(start, end + 1))
                    else:
                        page_numbers.add(int(part))
                
                # Check if all pages would be deleted
                if len(page_numbers) >= page_count:
                    print("❌ Cannot delete all pages. At least one page must remain.")
                    continue
                
                break
                
            except ValueError:
                print("❌ Invalid page format. Use numbers and ranges like: 1,3-5,7")
                continue
        
        output_file = input("\nEnter output filename (default: <filename>_modified.pdf): ").strip()
        if not output_file:
            base_name = os.path.splitext(file_path)[0]
            output_file = f"{base_name}_modified.pdf"
        
        tool.delete_pages(file_path, pages_input, output_file)
        
    except Exception as e:
        print(f"❌ Error: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="PDF Tool - Merge PDFs and delete pages from PDFs",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Interactive mode
  python pdf_tool.py

  # Merge PDFs
  python pdf_tool.py merge file1.pdf file2.pdf file3.pdf -o merged.pdf

  # Delete pages
  python pdf_tool.py delete input.pdf -p "1,3-5,7" -o output.pdf

  # Get page count
  python pdf_tool.py info file.pdf
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Merge command
    merge_parser = subparsers.add_parser('merge', help='Merge multiple PDF files')
    merge_parser.add_argument('files', nargs='+', help='Input PDF files')
    merge_parser.add_argument('-o', '--output', help='Output PDF file (default: merged.pdf)')
    
    # Delete command
    delete_parser = subparsers.add_parser('delete', help='Delete pages from a PDF file')
    delete_parser.add_argument('file', help='Input PDF file')
    delete_parser.add_argument('-p', '--pages', required=True, 
                              help='Pages to delete (e.g., "1,3-5,7")')
    delete_parser.add_argument('-o', '--output', help='Output PDF file')
    
    # Info command
    info_parser = subparsers.add_parser('info', help='Get information about a PDF file')
    info_parser.add_argument('file', help='PDF file to analyze')
    
    args = parser.parse_args()
    
    # If no command is provided, run interactive mode
    if not args.command:
        print("PDF Tool - Command Line Interface")
        print("==================================")
        
        while True:
            print("\nChoose an option:")
            print("1. Merge PDFs")
            print("2. Delete pages from PDF")
            print("3. Exit")
            
            choice = input("\nEnter your choice (1-3): ").strip()
            
            if choice == '1':
                interactive_merge()
            elif choice == '2':
                interactive_delete()
            elif choice == '3':
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please enter 1, 2, or 3.")
        
        return
    
    # Command-line mode
    tool = PDFTool()
    
    try:
        if args.command == 'merge':
            tool.merge_pdfs(args.files, args.output)
            
        elif args.command == 'delete':
            tool.delete_pages(args.file, args.pages, args.output)
            
        elif args.command == 'info':
            page_count = tool.get_page_count(args.file)
            file_size = os.path.getsize(args.file)
            print(f"File: {args.file}")
            print(f"Pages: {page_count}")
            print(f"Size: {file_size:,} bytes ({file_size / 1024:.1f} KB)")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 