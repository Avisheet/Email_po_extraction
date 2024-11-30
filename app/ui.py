from flask import Flask, request, render_template
from .email_handler import extract_email_content
from .iterative_classifier import iterative_classification
from .po_extraction import extract_po_details
from .setup_model import setup_llama

app = Flask(__name__)


text_gen_model, classifier = setup_llama()

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        subject = request.form.get("subject")
        body = request.form.get("body")
        
        
        classification, score = iterative_classification(subject, body, classifier)
        
        if classification == "PO":
            po_details = extract_po_details(body, text_gen_model)
            return render_template("results.html", po_details=po_details, score=score)
        
        return render_template("results.html", classification=classification, score=score)
    
    return render_template("index.html")
