from flask import Flask, request
from datetime import datetime
import os
import json

app = Flask(__name__)

@app.route("/admin", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
def admin_honeypot():

    log = {
        "timestamp": datetime.utcnow().isoformat(),
        "ip": request.headers.get("X-Forwarded-For", request.remote_addr),
        "method": request.method,
        "url": request.url,
        "path": request.path,
        "query": request.query_string.decode(errors="ignore"),
        "headers": dict(request.headers),
        "user_agent": request.headers.get("User-Agent"),
        "cookies": request.cookies.to_dict(),
        "body": request.get_data(as_text=True),
        "json": request.get_json(silent=True),
        "form": request.form.to_dict(),
        "files": list(request.files.keys()),
        "content_type": request.content_type,
    }

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    log_path = os.path.join(BASE_DIR, "../db", "log.ndjson")

    os.makedirs(os.path.dirname(log_path), exist_ok=True)

    try:
        
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(log) + "\n")
            f.flush()


    except Exception as e:
        print("LOG ERROR:", e)


    return "Unauthorized", 401

