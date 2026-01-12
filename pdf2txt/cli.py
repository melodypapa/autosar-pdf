"""
Command line interface for pdf2txt
"""
import argparse
import os
import sys
from pathlib import Path
from .core import convert_pdf_to_text, convert_pdf_to_text_advanced


def main():
    parser = argparse.ArgumentParser(
        description="Convert PDF files to text format"
    )
    parser.add_argument(
        "input",
        help="Input PDF file or directory containing PDF files"
    )
    parser.add_argument(
        "-o", "--output",
        help="Output file or directory for converted text files"
    )
    parser.add_argument(
        "-m", "--method",
        choices=["pymupdf", "pdfplumber"],
        default="pymupdf",
        help="Method to use for PDF conversion (default: pymupdf)"
    )
    parser.add_argument(
        "-p", "--pages",
        help="Specific pages to extract (e.g., '0,1,3' for pages 1,2,4 or '0-5' for pages 1-6)"
    )
    parser.add_argument(
        "--include-images",
        action="store_true",
        help="Include image metadata in the output"
    )
    parser.add_argument(
        "-f", "--force",
        action="store_true",
        help="Overwrite existing output files"
    )

    args = parser.parse_args()

    input_path = Path(args.input)

    # Handle single file or directory
    if input_path.is_file():
        if input_path.suffix.lower() != ".pdf":
            print(f"Error: {input_path} is not a PDF file")
            sys.exit(1)
        
        handle_single_pdf(input_path, args)
    elif input_path.is_dir():
        handle_pdf_directory(input_path, args)
    else:
        print(f"Error: {input_path} does not exist")
        sys.exit(1)


def parse_page_range(page_str):
    """
    Parse page range string like '0,1,3' or '0-5' or '2-4,7,9'
    Returns a list of 0-indexed page numbers
    """
    if not page_str:
        return None
    
    result = []
    parts = page_str.split(',')
    for part in parts:
        if '-' in part:
            start, end = map(int, part.split('-'))
            result.extend(range(start, end + 1))
        else:
            result.append(int(part))
    
    # Convert to 0-indexed
    return [p - 1 for p in result if p >= 0]


def handle_single_pdf(pdf_path, args):
    """Handle conversion of a single PDF file"""
    output_path = args.output
    
    # If no output specified, create output path based on input
    if not output_path:
        output_path = pdf_path.with_suffix('.txt')
    else:
        output_path = Path(output_path)
        # If output is a directory, create txt file inside it
        if output_path.is_dir():
            output_path = output_path / pdf_path.with_suffix('.txt').name
    
    # Check if output file already exists
    if output_path.exists() and not args.force:
        print(f"Output file {output_path} already exists. Use -f to overwrite or specify a different output.")
        return
    
    try:
        # Parse page range if specified
        page_range = parse_page_range(args.pages)
        
        # Convert PDF to text
        if page_range or args.include_images:
            result = convert_pdf_to_text_advanced(
                str(pdf_path),
                page_range=page_range,
                include_images=args.include_images
            )
            text = result["text"]
        else:
            text = convert_pdf_to_text(str(pdf_path), method=args.method)
        
        # Write to output file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(text)
        
        print(f"Successfully converted {pdf_path} to {output_path}")
        
        if args.include_images and 'images' in result:
            print(f"Found {len(result['images'])} images in the PDF")
        
    except Exception as e:
        print(f"Error converting {pdf_path}: {str(e)}")
        sys.exit(1)


def handle_pdf_directory(pdf_dir, args):
    """Handle conversion of all PDF files in a directory"""
    pdf_dir = Path(pdf_dir)
    output_dir = Path(args.output) if args.output else pdf_dir
    
    # Create output directory if it doesn't exist
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Find all PDF files in the directory
    pdf_files = list(pdf_dir.glob("*.pdf"))
    
    if not pdf_files:
        print(f"No PDF files found in {pdf_dir}")
        return
    
    print(f"Found {len(pdf_files)} PDF files to convert")
    
    for pdf_file in pdf_files:
        # Create output path in the output directory
        output_path = output_dir / pdf_file.with_suffix('.txt').name
        
        # Skip if output file exists and force flag is not set
        if output_path.exists() and not args.force:
            print(f"Skipping {pdf_file} (output already exists, use -f to overwrite)")
            continue
        
        try:
            text = convert_pdf_to_text(str(pdf_file), method=args.method)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(text)
            
            print(f"Converted: {pdf_file.name} -> {output_path.name}")
        
        except Exception as e:
            print(f"Error converting {pdf_file}: {str(e)}")


if __name__ == "__main__":
    main()