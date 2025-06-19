# PDF Tool - Command Line Interface

A simple command-line tool for merging PDFs and deleting pages from PDFs.

## Installation

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Make the script executable (optional):**
   ```bash
   chmod +x pdf_tool.py
   ```

## Usage

### Interactive Mode

Run the tool without arguments to enter interactive mode:

```bash
python pdf_tool.py
```

This will present you with a menu to choose between:
1. Merge PDFs
2. Delete pages from PDF
3. Exit

### Command Line Mode

#### Merge PDFs

```bash
# Basic merge (outputs to merged.pdf)
python pdf_tool.py merge file1.pdf file2.pdf file3.pdf

# Specify output file
python pdf_tool.py merge file1.pdf file2.pdf -o combined.pdf
```

#### Delete Pages

```bash
# Delete specific pages
python pdf_tool.py delete input.pdf -p "1,3,5"

# Delete page ranges
python pdf_tool.py delete input.pdf -p "1-3,7-9"

# Mixed single pages and ranges
python pdf_tool.py delete input.pdf -p "1,3-5,7,9-12"

# Specify output file
python pdf_tool.py delete input.pdf -p "1,3-5" -o cleaned.pdf
```

#### Get PDF Information

```bash
python pdf_tool.py info document.pdf
```

## Page Numbering

- Pages are numbered starting from 1 (not 0)
- You can specify individual pages: `1,3,5`
- You can specify ranges: `1-5` (includes pages 1, 2, 3, 4, 5)
- You can mix both: `1,3-5,7,9-12`

## Examples

### Merge Multiple PDFs
```bash
python pdf_tool.py merge chapter1.pdf chapter2.pdf chapter3.pdf -o complete_book.pdf
```

### Delete First and Last Pages
```bash
python pdf_tool.py delete document.pdf -p "1,10" -o document_clean.pdf
```

### Delete a Range of Pages
```bash
python pdf_tool.py delete presentation.pdf -p "1-3,8-10" -o presentation_final.pdf
```

### Get Information About a PDF
```bash
python pdf_tool.py info large_document.pdf
# Output:
# File: large_document.pdf
# Pages: 150
# Size: 2,500,000 bytes (2441.4 KB)
```

## Error Handling

The tool includes comprehensive error handling for:
- File not found errors
- Invalid PDF files
- Invalid page numbers
- Insufficient files for merging
- Attempting to delete all pages

## Features

- ✅ Merge multiple PDF files
- ✅ Delete specific pages or page ranges
- ✅ Interactive mode for easy use
- ✅ Command-line mode for automation
- ✅ Get PDF information (page count, file size)
- ✅ Automatic output filename generation
- ✅ Comprehensive error handling
- ✅ Progress indicators
- ✅ Input validation

## Requirements

- Python 3.6+
- PyPDF2 library

## Troubleshooting

### Common Issues

1. **"File not found" error:**
   - Make sure the file path is correct
   - Use absolute paths if needed

2. **"File is not a PDF" error:**
   - Ensure the file has a `.pdf` extension
   - Verify the file is actually a valid PDF

3. **"Invalid page numbers" error:**
   - Page numbers must be between 1 and the total number of pages
   - Use the `info` command to check page count first

4. **"Cannot delete all pages" error:**
   - At least one page must remain in the PDF
   - Check your page selection

### Getting Help

Run the tool with `-h` or `--help` to see all available options:

```bash
python pdf_tool.py --help
python pdf_tool.py merge --help
python pdf_tool.py delete --help
python pdf_tool.py info --help
``` 