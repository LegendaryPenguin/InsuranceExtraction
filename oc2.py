import fitz  # PyMuPDF
import re

def extract_text_from_pdf(pdf_path):
    """
    Extracts text directly from a PDF file using PyMuPDF.
    
    Args:
    - pdf_path (str): Path to the PDF file.
    
    Returns:
    - list: Extracted text lines from the PDF, cleaned of extra spaces.
    """
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text("text")  # Extract selectable text
    return [line.strip() for line in text.split("\n") if line.strip()]

def parse_claim_data(lines):
    """
    Extracts only the fields that a human would input from a structured CMS-1500 form.
    Ensures missing values are replaced with "Flag for Review".
    """
    claim_data = {
        "Patient Name": lines[0] if len(lines) > 0 else "Flag for Review",
        "Date of Birth": f"{lines[1]}/{lines[2]}/{lines[3]}" if len(lines) > 3 else "Flag for Review",
        "Gender": lines[4] if len(lines) > 4 else "Flag for Review",
        "Address": lines[5] if len(lines) > 5 else "Flag for Review",
        "City": lines[6] if len(lines) > 6 else "Flag for Review",
        "State": lines[7] if len(lines) > 7 else "Flag for Review",
        "ZIP Code": lines[8] if len(lines) > 8 else "Flag for Review",
        "Phone Number": lines[9] if len(lines) > 9 else "Flag for Review",
        "Insurance Name": lines[10] if len(lines) > 10 else "Flag for Review",
        "Insurance ID": lines[11] if len(lines) > 11 else "Flag for Review",
        "Policy Number": lines[12] if len(lines) > 12 else "Flag for Review",
        "Group Number": lines[13] if len(lines) > 13 else "Flag for Review",
        "Physician Name": lines[14] if len(lines) > 14 else "Flag for Review",
        "Physician NPI": lines[15] if len(lines) > 15 else "Flag for Review",
        "Facility Name": lines[16] if len(lines) > 16 else "Flag for Review",
        "Facility Address": lines[17] if len(lines) > 17 else "Flag for Review",
        "Date of Service Start": lines[18] if len(lines) > 18 else "Flag for Review",
        "Date of Service End": lines[19] if len(lines) > 19 else "Flag for Review",
        "Diagnosis Codes": lines[20] if len(lines) > 20 else "Flag for Review",
        "Procedure Codes": lines[21] if len(lines) > 21 else "Flag for Review",
        "Claim Amount": lines[22] if len(lines) > 22 else "Flag for Review",
        "Prior Authorization Number": lines[23] if len(lines) > 23 else "Flag for Review",
        "Claim Type": lines[24] if len(lines) > 24 else "Flag for Review",
        "Accident Information": lines[25] if len(lines) > 25 else "Flag for Review"
    }
    return claim_data

# Example usage
pdf_path = r"C:\Users\nisch\OneDrive\Desktop\verisure\samples\sample_claim.pdf"
lines = extract_text_from_pdf(pdf_path)

# Parse claim data
claim_data = parse_claim_data(lines)

print("\nExtracted Claim Information:")
for key, value in claim_data.items():
    print(f"{key}: {value}")