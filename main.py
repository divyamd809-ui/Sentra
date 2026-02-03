from src.api.route import app
from src.tools.log_analyser import AnalyseLog


import os


def main():

    # if __name__ == "__main__":

    #     app.run(
    #         host="0.0.0.0",
    #         port=5000,
    #         debug=True,
    #         use_reloader=False
    #     )


    log_path = os.path.join(os.path.dirname(__file__), "src", "db", "log.ndjson")
    log_path = os.path.abspath(log_path)

    if not os.path.exists(log_path):
        print(f"Log file not found: {log_path}")
        return

    with open(log_path, "r", encoding="utf-8") as f:
        logs = f.read()

    try:
        AnalyseLog(logs)
    except Exception as e:
        print("AnalyseLog failed:", type(e).__name__, e)


main()