import os
import json
import threading
from datetime import datetime
from flask import Flask, send_from_directory, jsonify, request
from src.tools.log_analyser import AnalyseLog

app = Flask(__name__, 
            static_folder=os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'frontend')),
            static_url_path='')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
log_path = os.path.join(BASE_DIR, "src", "db", "log.ndjson")
report_path = os.path.join(BASE_DIR, "src", "db", "report.json")

# Ensure db directory exists
os.makedirs(os.path.dirname(log_path), exist_ok=True)

@app.route("/")
def dashboard():
    return send_from_directory(app.static_folder, "index.html")

# Integrated Honeypot Route
@app.route("/admin", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
@app.route("/admin/<path:subpath>", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
def admin_honeypot(subpath=""):
    log = {
        "timestamp": datetime.utcnow().isoformat(),
        "ip": request.headers.get("X-Forwarded-For", request.remote_addr),
        "method": request.method,
        "url": request.url,
        "path": request.path,
    }
    try:
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(log) + "\n")
            f.flush()
    except Exception as e:
        print("LOG ERROR:", e)
    return "Unauthorized", 401

@app.route("/api/logs")
def get_logs():
    try:
        if not os.path.exists(log_path):
            return jsonify([])
        logs = []
        with open(log_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
            for line in reversed(lines[-50:]): # Get last 50 logs for live view
                if line.strip():
                    try:
                        log_entry = json.loads(line)
                        if "admin" in log_entry.get("path", ""):
                            log_entry["severity"] = "Critical"
                        logs.append(log_entry)
                    except json.JSONDecodeError:
                        continue
        return jsonify(logs)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/report")
def get_report():
    try:
        if not os.path.exists(report_path):
            return jsonify({"status": "pending", "message": "Analyzing logs, please wait..."})
        with open(report_path, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if not content:
                return jsonify({"status": "pending", "message": "Analyzing logs, please wait..."})
            return jsonify({"status": "success", "raw_report": content})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/raw-logs")
def get_raw_logs():
    try:
        if not os.path.exists(log_path):
            return jsonify({"content": "No logs generated yet."})
        with open(log_path, "r", encoding="utf-8") as f:
            content = f.read()
        return jsonify({"content": content})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/analyze", methods=["POST"])
def trigger_analysis():
    def run_analysis():
        try:
            if os.path.exists(log_path):
                with open(log_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    if len(content) > 10000:
                        content = content[-10000:] # feed recent logs
                AnalyseLog(content)
        except Exception as e:
            print("Background analysis failed:", e)
    
    threading.Thread(target=run_analysis).start()
    return jsonify({"status": "success", "message": "Analysis started in background!"})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
