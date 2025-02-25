import fitz  # PyMuPDF
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# Path to the fixed PDF file
pdf_path = r"C:\Users\nisch\OneDrive\Desktop\verisure\samples\sample_claim.pdf"

def extract_text_from_pdf(pdf_path):
    """Extracts text directly from a PDF file using PyMuPDF."""
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text("text")
    return [line.strip() for line in text.split("\n") if line.strip()]

def parse_claim_data(lines):
    """Extracts claim data from the extracted text."""
    claim_data = {}

    claim_data["Policy Holder Name"] = lines[118]  # Eth Den
    claim_data["Patient Name"] = lines[116]  # Eig Gam
    claim_data["Patient DOB"] = lines[117]  # 06/14/2000
    claim_data["Patient Sex"] = "Male" if "Male" in lines[10] else "Female"
    claim_data["Policy Holder DOB"] = lines[119]  # 06/14/1973

    relationship = "Flag for Review"
    if "Spouse" in lines[16]:  
        relationship = "Spouse"
    claim_data["Relationship to Enrollee"] = relationship

    claim_data["Address"] = lines[120]
    claim_data["Email"] = lines[121]

    claim_data["Medicare Part A Effective"] = lines[123]
    claim_data["Medicare Part B Effective"] = lines[124]
    claim_data["Medicare HMO Effective"] = lines[125]

    claim_data["ESRD Date"] = lines[126]

    accident_date = lines[65]
    if accident_date != "5A. DATE OF ACCIDENT":
        claim_data["Accident Date"] = accident_date
    else:
        claim_data["Accident Date"] = "Flag for Review"

    claim_data["Provider Name"] = lines[127]
    claim_data["Service Description"] = lines[128]
    claim_data["Date of Service From"] = lines[129]
    claim_data["Charge Amount"] = lines[130]
    claim_data["Phone Number"] = lines[133]

    policy_number = "".join(lines[107:116])
    claim_data["Policy Number"] = policy_number

    return claim_data

@app.route("/", methods=["GET"])
def welcome():
    return "Welcome to the Gaia Processing API! Use /process or /process_fixed to access the functionality."

@app.route("/process_fixed", methods=["GET"])
def handle_fixed_pdf_processing():
    """Handles processing of a fixed PDF file and returns the extracted claim data."""
    lines = extract_text_from_pdf(pdf_path)
    claim_data = parse_claim_data(lines)

    # Create a simple HTML representation of the extracted data
    html_content = "<h1>Extracted Claim Data</h1>"
    for key, value in claim_data.items():
        html_content += f"<p><strong>{key}:</strong> {value}</p>"
    
    return render_template_string(html_content)

@app.route("/process", methods=["POST"])
def handle_pdf_processing():
    """Handles PDF upload, extracts text, and processes claim data."""
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    pdf_file = request.files["file"]
    pdf_path = f"/tmp/{pdf_file.filename}"  
    pdf_file.save(pdf_path)

    lines = extract_text_from_pdf(pdf_path)
    claim_data = parse_claim_data(lines)

    return jsonify(claim_data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
