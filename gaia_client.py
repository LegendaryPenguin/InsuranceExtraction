import requests

GAIA_NODE_URL = "https://0x8600b7fb770322a38c1ba3e8fcab1f73c6cc701b.gaia.domains/process"

def send_pdf_to_gaia(pdf_path):
    """Sends a PDF file to the Gaia node for full text extraction and claim processing."""
    with open(pdf_path, "rb") as f:
        files = {"file": f}
        response = requests.post(GAIA_NODE_URL, files=files)
    
    if response.status_code == 200:
        return response.json()  # Processed claim data
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None

# Example usage
pdf_path = r"C:\Users\nisch\OneDrive\Desktop\verisure\samples\sample_claim.pdf"
processed_data = send_pdf_to_gaia(pdf_path)

print("\nProcessed Claim Data from Gaia Node:\n", processed_data)
