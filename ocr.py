import pytesseract
import os
import fitz  # PyMuPDF
from PIL import Image  # Import Pillow (PIL) for image handling
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set the path for Tesseract OCR if provided in .env file
TESSERACT_PATH = os.getenv("TESSERACT_PATH")
if TESSERACT_PATH:
    pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH
    print(f"Tesseract path set to: {TESSERACT_PATH}")  # Debugging line
else:
    print("TESSERACT_PATH not found in .env file. OCR may not work.")

def extract_text_from_pdf(pdf_path):
    """
    Extracts text from a PDF file by converting each page to an image using PyMuPDF and applying OCR.

    Args:
    - pdf_path (str): Path to the PDF file.

    Returns:
    - str: Extracted text from the PDF, or None if an error occurs.
    """
    try:
        print(f"Processing PDF: {pdf_path}")  # Debugging line
        # Open the PDF file using PyMuPDF
        pdf_document = fitz.open(pdf_path)
        text = ""

        for page_number in range(pdf_document.page_count):
            page = pdf_document.load_page(page_number)
            print(f"Processing page {page_number + 1}...")  # Debugging line

            # Convert page to a pixmap
            pix = page.get_pixmap()

            # Convert the pixmap to a PIL Image object
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

            # Image Preprocessing
            img = img.convert('L')  # Convert to grayscale

            # Use pytesseract to extract text from the Image object
            page_text = pytesseract.image_to_string(img, config='--psm 6')
            text += page_text

            print(f"Page {page_number + 1} processed.")  # Debugging line

        print("OCR extraction completed.")  # Debugging line
        return text

    except Exception as e:
        print(f"OCR Error: {e}")
        return None  # Return None if OCR fails

# Example usage (make sure you provide a valid path to a PDF):
pdf_path = r"C:\Users\nisch\OneDrive\Desktop\verisure\samples\sample_claim.pdf"  # Update with your PDF file path
pdf_text = extract_text_from_pdf(pdf_path)

# Print extracted text or a failure message
if pdf_text:
    print("\nExtracted text from PDF:")
    print(pdf_text)
else:
    print("No text extracted.")
