"""
app.py  —  Sentiment Analysis Tool
Routes: / login signup signup-api login-api logout dashboard analyse upload report
"""

import os, io, csv, json, smtplib, hashlib, secrets
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from functools import wraps

from flask import (Flask, render_template, request, jsonify,
                   session, redirect, url_for, send_file)
from sentiment_engine import SentimentEngine
from report_generator import generate_report

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)
engine = SentimentEngine()

MAIL_USER      = os.environ.get("MAIL_USER", "your@gmail.com")
MAIL_PASS      = os.environ.get("MAIL_PASS", "your_app_password")
MAIL_FROM_NAME = "SentiAI"
USERS_FILE     = os.path.join(os.path.dirname(__file__), "data", "users.json")

def _load_users():
    if not os.path.exists(USERS_FILE): return {}
    with open(USERS_FILE) as f: return json.load(f)

def _save_users(u):
    os.makedirs(os.path.dirname(USERS_FILE), exist_ok=True)
    with open(USERS_FILE,"w") as f: json.dump(u,f,indent=2)

def _hash(p): return hashlib.sha256(p.encode()).hexdigest()

def login_required(f):
    @wraps(f)
    def dec(*a,**k):
        if "user" not in session: return redirect(url_for("login_page"))
        return f(*a,**k)
    return dec

@app.route("/")
def landing(): return render_template("landing.html")

@app.route("/login")
def login_page():
    if "user" in session: return redirect(url_for("dashboard"))
    return render_template("login.html")

@app.route("/signup")
def signup_page():
    if "user" in session: return redirect(url_for("dashboard"))
    return render_template("signup.html")

@app.route("/logout")
def logout():
    session.clear(); return redirect(url_for("landing"))

@app.route("/dashboard")
@login_required
def dashboard(): return render_template("dashboard.html", user=session["user"])

@app.route("/api/signup", methods=["POST"])
def api_signup():
    d=request.get_json()
    name=d.get("name","").strip(); email=d.get("email","").strip().lower(); password=d.get("password","").strip()
    if not name or not email or not password: return jsonify({"error":"All fields required."}),400
    if len(password)<6: return jsonify({"error":"Password must be at least 6 characters."}),400
    users=_load_users()
    if email in users: return jsonify({"error":"Email already registered."}),409
    users[email]={"name":name,"email":email,"password":_hash(password),"created":datetime.now().isoformat()}
    _save_users(users)
    try: _send_welcome_email(name, email, password)
    except Exception as e: print(f"[Email] {e}")
    session["user"]={"name":name,"email":email}
    return jsonify({"success":True,"redirect":"/dashboard"})

@app.route("/api/login", methods=["POST"])
def api_login():
    d=request.get_json()
    email=d.get("email","").strip().lower(); password=d.get("password","").strip()
    users=_load_users(); user=users.get(email)
    if not user or user["password"]!=_hash(password): return jsonify({"error":"Invalid email or password."}),401
    session["user"]={"name":user["name"],"email":email}
    return jsonify({"success":True,"redirect":"/dashboard"})

@app.route("/api/analyse", methods=["POST"])
@login_required
def analyse():
    data=request.get_json(); reviews=data.get("reviews",[])
    if not reviews: return jsonify({"error":"No reviews provided"}),400
    results=[engine.predict(r) for r in reviews]
    return jsonify({"results":results,"summary":_build_summary(results)})

@app.route("/api/upload", methods=["POST"])
@login_required
def upload():
    file=request.files.get("file")
    if not file: return jsonify({"error":"No file uploaded"}),400
    content=file.read().decode("utf-8",errors="ignore")
    reader=csv.reader(io.StringIO(content))
    reviews=[row[0].strip() for row in reader if row and row[0].strip() and row[0].strip().lower() not in ("text","review","comment")]
    if not reviews: return jsonify({"error":"No text found in CSV"}),400
    results=[engine.predict(r) for r in reviews]
    return jsonify({"results":results,"summary":_build_summary(results)})

@app.route("/api/report", methods=["POST"])
@login_required
def report():
    data=request.get_json(); results=data.get("results",[]); summary=data.get("summary",{})
    if not results: return jsonify({"error":"No results provided"}),400
    pdf_bytes=generate_report(results,summary)
    filename=f"sentiment_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    return send_file(io.BytesIO(pdf_bytes),mimetype="application/pdf",as_attachment=True,download_name=filename)

def _send_welcome_email(name, email, password):
    msg=MIMEMultipart("alternative")
    msg["Subject"]="Welcome to SentiAI — Your Login Details"
    msg["From"]=f"{MAIL_FROM_NAME} <{MAIL_USER}>"; msg["To"]=email
    html=f"""<!DOCTYPE html><html><body style="margin:0;padding:0;background:#0d0d0d;font-family:'Segoe UI',sans-serif;">
<table width="100%" cellpadding="0" cellspacing="0" style="background:#0d0d0d;padding:40px 20px;"><tr><td align="center">
<table width="580" cellpadding="0" cellspacing="0" style="background:#111;border-radius:16px;overflow:hidden;border:1px solid #222;">
<tr><td style="background:linear-gradient(135deg,#00ff88,#00ccff);padding:40px;text-align:center;">
<h1 style="margin:0;font-size:32px;color:#0d0d0d;font-weight:900;letter-spacing:-1px;">SENTI<span style="opacity:.6">AI</span></h1>
<p style="margin:8px 0 0;color:#0d0d0d;font-size:14px;opacity:.7;">Customer Sentiment Intelligence</p></td></tr>
<tr><td style="padding:40px;">
<h2 style="color:#fff;font-size:22px;margin:0 0 8px;">Welcome, {name}! 🎉</h2>
<p style="color:#aaa;font-size:15px;line-height:1.7;margin:0 0 28px;">Your SentiAI account is ready. Here are your login credentials — keep them safe!</p>
<table width="100%" cellpadding="0" cellspacing="0" style="background:#1a1a1a;border:1px solid #2a2a2a;border-radius:10px;margin-bottom:28px;">
<tr><td style="padding:20px 24px;">
<p style="margin:0 0 4px;color:#555;font-size:11px;text-transform:uppercase;letter-spacing:.08em;">Email</p>
<p style="margin:0 0 16px;color:#00ff88;font-size:15px;font-weight:600;">{email}</p>
<p style="margin:0 0 4px;color:#555;font-size:11px;text-transform:uppercase;letter-spacing:.08em;">Password</p>
<p style="margin:0;color:#00ff88;font-size:15px;font-weight:600;">{password}</p></td></tr></table>
<table cellpadding="0" cellspacing="0" style="margin:0 auto 28px;"><tr>
<td style="background:linear-gradient(135deg,#00ff88,#00ccff);border-radius:8px;">
<a href="http://localhost:5000/login" style="display:block;padding:14px 36px;color:#0d0d0d;font-weight:700;font-size:15px;text-decoration:none;">Launch SentiAI →</a>
</td></tr></table>
<p style="color:#444;font-size:13px;text-align:center;margin:0;">Change your password after first login for security.</p>
</td></tr>
<tr><td style="background:#0a0a0a;padding:20px;text-align:center;border-top:1px solid #1a1a1a;">
<p style="color:#333;font-size:12px;margin:0;">© {datetime.now().year} SentiAI · Customer Sentiment Intelligence Platform</p>
</td></tr></table></td></tr></table></body></html>"""
    msg.attach(MIMEText(html,"html"))
    with smtplib.SMTP_SSL("smtp.gmail.com",465) as s:
        s.login(MAIL_USER,MAIL_PASS); s.sendmail(MAIL_USER,email,msg.as_string())
    print(f"[Email] Sent to {email}")

def _build_summary(results):
    total=len(results); counts={"Positive":0,"Negative":0,"Neutral":0}
    for r in results: counts[r["sentiment"]]+=1
    percentages={k:round(v/total*100,1) if total else 0 for k,v in counts.items()}
    return {"total":total,"counts":counts,"percentages":percentages,"dominant":max(counts,key=counts.get)}
  
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
