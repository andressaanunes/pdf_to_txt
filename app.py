import pandas as pd
import requests
from flask import Flask, request, Response, render_template
import PyPDF2
import json

app = Flask(__name__)

@app.route("/", methods=["POST"])
def template():
    render_template("index.html")
    
def convert_pdf_to_txt():
    """
    API endpoint to convert uploaded PDF to TXT format.
    Expects a multipart form data with the PDF file in the "pdf_file" field.
    """

    # Get the uploaded PDF file
    pdf_file =  request.files['pdf_file']
    print(pdf_file)

    if not pdf_file:
        return Response(json.dumps({"error": "No PDF file uploaded"}), status=400)

    try:
        # Open the PDF file
        # with pdf_file.open(mode="rb") as f:
        pdf_reader = PyPDF2.PdfReader(pdf_file)

        # Extract text from all pages
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()

        response = Response(text, mimetype='text/plain')
        response.headers['Content-Disposition'] = f'attachment; filename={pdf_file.name}.txt'
        return response

    except Exception as e:
        return Response(json.dumps({"error": f"Error processing PDF: {str(e)}"}), status=500)


if __name__ == "__main__":
    app.run(port=8000) 
# Set debug=False for production