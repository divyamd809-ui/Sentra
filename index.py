from flask import Flask, render_template

app = Flask(__name__)

# Example log data (Replace with real data later)
logs = [
    {"ip": "192.168.1.10", "attack": "Brute Force", "severity": "High"},
    {"ip": "10.0.0.5", "attack": "SQL Injection", "severity": "Critical"},
    {"ip": "172.16.0.8", "attack": "XSS", "severity": "Medium"}
]

@app.route("/")
def dashboard():
    return render_template("dashboard.html", logs=logs)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
