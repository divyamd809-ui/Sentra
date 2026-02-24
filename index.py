from flask import Flask, render_template

app = Flask(__name__)

# Sample SOC logs
logs = [
    {"ip": "192.168.1.10", "attack": "Brute Force", "severity": "High"},
    {"ip": "10.0.0.5", "attack": "SQL Injection", "severity": "Critical"},
    {"ip": "172.16.0.8", "attack": "XSS", "severity": "Medium"},
    {"ip": "192.168.5.2", "attack": "DDoS", "severity": "Critical"}
]

@app.route("/")
def dashboard():
    return render_template("dashboard.html", logs=logs)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
njnnkmlkpkpk,;,;l;l