from flask import Flask, render_template, request, send_file
from PyPDF2 import PdfMerger, PdfReader, PdfWriter
from pdf2docx import Converter
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/compress', methods=['POST'])
def compress_pdf():
    pdf_file = request.files['pdf']
    file_path = os.path.join(UPLOAD_FOLDER, pdf_file.filename)
    pdf_file.save(file_path)

    reader = PdfReader(file_path)
    writer = PdfWriter()
    for page in reader.pages:
        writer.add_page(page)

    compressed_path = os.path.join(UPLOAD_FOLDER, "compressed_" + pdf_file.filename)
    with open(compressed_path, "wb") as f:
        writer.write(f)

    return send_file(compressed_path, as_attachment=True)

@app.route('/merge', methods=['POST'])
def merge_pdf():
    files = request.files.getlist('pdfs')
    merger = PdfMerger()
    for file in files:
        path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(path)
        merger.append(path)
    merged_path = os.path.join(UPLOAD_FOLDER, "merged.pdf")
    merger.write(merged_path)
    merger.close()
    return send_file(merged_path, as_attachment=True)

@app.route('/convert', methods=['POST'])
def convert_pdf_to_doc():
    file = request.files['pdf']
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    docx_path = os.path.join(UPLOAD_FOLDER, file.filename.replace('.pdf', '.docx'))
    converter = Converter(file_path)
    converter.convert(docx_path)
    converter.close()

    return send_file(docx_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)