from flask import Flask, render_template, request, send_file
import qrcode
import os
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/invite")
def invite():
    groom = request.args.get("groom", "Sujeet")
    bride = request.args.get("bride", "Priya")
    date = request.args.get("date", "25 March 2026")
    venue = request.args.get("venue", "Indore")

    return render_template("invite.html",
                           groom=groom,
                           bride=bride,
                           date=date,
                           venue=venue)

@app.route("/generate")
def generate():
    groom = request.args.get("groom", "Sujeet")
    bride = request.args.get("bride", "Priya")

    link = f"http://10.149.7.25:5000/invite?groom={groom}&bride={bride}"

    if not os.path.exists("static"):
        os.makedirs("static")

    qr_path = "static/qr.png"
    qr = qrcode.make(link)
    qr.save(qr_path)

    pdf_path = "invitation.pdf"
    doc = SimpleDocTemplate(pdf_path, pagesize=A4)
    elements = []

    style = ParagraphStyle(name='Normal', fontSize=22)

    elements.append(Spacer(1, 1*inch))
    elements.append(Paragraph(f"{groom} ❤️ {bride}", style))
    elements.append(Spacer(1, 0.5*inch))
    elements.append(Image(qr_path, 2*inch, 2*inch))

    doc.build(elements)

    return send_file(pdf_path, as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)