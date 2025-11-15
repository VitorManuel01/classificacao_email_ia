import logging

from ai_provider import AIProvider
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json
from io import BytesIO
from PyPDF2 import PdfFileReader, PdfFileWriter
from waitress import serve

# Try imports compatible com diferentes versões do PyPDF2
try:
    # Versões mais novas de PyPDF2
    from PyPDF2 import PdfReader

    _HAS_PDFREADER = True
except Exception:
    try:
        # Versões antigas
        from PyPDF2 import PdfFileReader

        _HAS_PDFREADER = False
    except Exception:
        PdfReader = None
        PdfFileReader = None
        _HAS_PDFREADER = None

# Configurar logging básico
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
# Enable CORS
CORS(app)

# Initialize AI Provider
ia = AIProvider(provider="gemini")


# extract text from pdf bytes, necessary for file upload handling
def extract_text_from_pdf_bytes(b: bytes) -> str:
    """
    Tenta extrair texto de bytes de PDF usando PdfReader (PyPDF2 moderna).
    Faz fallback para PdfFileReader em versões antigas. Retorna string vazia em erro.
    """
    try:
        stream = BytesIO(b)
        text_parts = []

        if _HAS_PDFREADER is True and 'PdfReader' in globals() and PdfReader is not None:
            # API moderna
            reader = PdfReader(stream)
            pages = getattr(reader, "pages", None)
            if pages is None:
                # segurança extra
                for i in range(len(reader.pages)):
                    page = reader.pages[i]
                    text_parts.append(page.extract_text() or "")
            else:
                for page in pages:
                    try:
                        text_parts.append(page.extract_text() or "")
                    except Exception:
                        # continue on page errors
                        logger.exception("Erro extraindo texto de uma página com PdfReader")
                        continue
        elif _HAS_PDFREADER is False and 'PdfFileReader' in globals() and PdfFileReader is not None:
            # Fallback para API antiga
            reader = PdfFileReader(stream)
            num_pages = getattr(reader, "numPages", 0)
            for page_num in range(num_pages):
                try:
                    page = reader.getPage(page_num)
                    text_parts.append(page.extract_text() or "")
                except Exception:
                    logger.exception("Erro extraindo texto de uma página com PdfFileReader")
                    continue
        else:
            logger.error("Nenhuma implementação de PyPDF2 disponível para extração de PDF.")
            return ""

        text = "\n".join(text_parts).strip()
        return text
    except Exception as e:
        logger.exception("Falha ao extrair texto do PDF")
        return ""


# Flask endpoint setup to the api
@app.route('/analyze_email', methods=['POST'])
def analyse_email_portuguese():
    """Endpoint to analyze email content in Portuguese.
        userData: {
            username: str,
            fullName: str,
            email: str
        }

        emailText: str,
        file: File (optional, PDF file or text file)


        response is JSON with classification and suggested response.
    """
    try:
        # UserData JSON
        user_json = request.form.get('userData')
        if not user_json:  # if there is no user data a message will be shown
            return "Campo userData ausente", 400
        user_data = json.loads(user_json)  # successfully parse the user data

        # EmailData JSON
        email_text = request.form.get('email_text', "").strip()  # get email text from form data with no empty spaces
        if not email_text and 'file' in request.files:  # if there is no email text but a file was uploaded
            f = request.files["file"]  # get the uploaded file
            filename = f.filename.lower()  # get the filename in lowercase
            content = f.read()  # read the file content
            # check the file extension and extract text accordingly
            if filename.endswith('.pdf'):  # if the file is a pdf use the pdf text extractor
                email_text = extract_text_from_pdf_bytes(content)
            elif filename.endswith('.txt'):  # if the file is a text file decode it to string
                email_text = content.decode(errors='ignore')
            else:
                return "Formato de arquivo não suportado", 400
        if not email_text:
            return "Nenhum texto de email fornecido", 400

        sender_name = user_data.get('fullName')  # set sender name from user data
        company_name = "Tech Solutions"  # Hardcoded company name, can be modified as needed
        res = ia.analyze_email_portuguese(email_text, sender_name,
                                          company_name)  # analyze the email using the ai provider

        return jsonify({  # return the classification and suggested response as json
            "classification": res.get('classification'),
            "suggestedResponse": res.get('suggestedResponse')
        })
    except Exception as e:
        return str(e), 500


if __name__ == "__main__":
    # Run the Flask app with Waitress for production readiness

    serve(app, host="0.0.0.0", port=5000)
