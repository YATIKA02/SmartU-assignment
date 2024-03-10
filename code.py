from flask import Flask, render_template, request, jsonify
import os
import PyPDF2
import gensim.corpora as corpora
from gensim.models import TfidfModel
from gensim.summarization import keywords

app = Flask(__name__)

marathi_stopwords = set(["शहर", "राज्य", "सरकार", "विधानसभा", "सभा", "प्रधानमंत्री", "मंत्री", "या", "की", "और", "हे", "मिळवतात", "आहे", "होता", "हो"])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    if request.method == 'POST':
        pdf_file = request.files['pdf_file']
        filename = pdf_file.filename
        pdf_file.save(filename)

        pdf_reader = PyPDF2.PdfFileReader(open(filename, 'rb'))
        num_pages = pdf_reader.getNumPages()
        if num_pages < 15:
            os.remove(filename)
            return jsonify({'error': 'The PDF must have more than 15 pages.'}), 400

        text = ""
        for page in range(num_pages):
            page_obj = pdf_reader.getPage(page)
            text += page_obj.extractText()

        marathi_keywords = keywords(text, words=5, ratio=0.5, stopwords=marathi_stopwords)

        os.remove(filename)

        return jsonify({'keywords': marathi_keywords})

if __name__ == '__main__':
    app.run(debug=True)
