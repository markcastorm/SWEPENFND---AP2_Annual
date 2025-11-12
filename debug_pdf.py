import glob
import os
import sys
import fitz  # PyMuPDF
import logging
import config

logging.basicConfig(level=logging.INFO, format='%(message)s')

def extract_text_to_file(pdf_path, output_txt_path):
    """Extracts text from each page of a PDF and saves it to a text file."""
    if not os.path.exists(pdf_path):
        logging.error(f"PDF file not found at: {pdf_path}")
        return

    doc = fitz.open(pdf_path)
    with open(output_txt_path, "w", encoding="utf-8") as outfile:
        for i, page in enumerate(doc):
            text = page.get_text()
            outfile.write(f"--- PAGE {i+1} ---\n")
            outfile.write(text)
            outfile.write("\n\n")
    doc.close()
    logging.info(f"Successfully extracted text from {doc.page_count} pages to {output_txt_path}")

if __name__ == "__main__":
    # Use the latest timestamped folder
    download_folders = glob.glob(os.path.join(config.DOWNLOADS_DIR, '*'))
    if not download_folders:
        logger.error("No download folders found")
        sys.exit(1)

    latest_folder = max(download_folders, key=os.path.getmtime)
    
    pdf_files = glob.glob(os.path.join(latest_folder, '*.pdf'))
    if not pdf_files:
        logger.error(f"No PDF files found in {latest_folder}")
        sys.exit(1)
        
    pdf_path = pdf_files[0]
    logger.info(f"Analyzing PDF: {pdf_path}")

    output_path = os.path.join(config.PROJECT_ROOT, "debug_pdf_text.txt")
    extract_text_to_file(pdf_path, output_path)