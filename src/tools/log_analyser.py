from langchain_openai import ChatOpenAI
from src.prompt.tools_prompt import logAnalyserPrompt

from dotenv import load_dotenv
import os


load_dotenv()


def AnalyseLog(log):

    prompt = logAnalyserPrompt(log)

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    report_path = os.path.join(BASE_DIR, "../db", "report.json")

    llm = ChatOpenAI(
        model= os.getenv("MODEL"),
        base_url= os.getenv("BASE_URL"),
        api_key= os.getenv("API_KEY")
    )

    response = llm.invoke(prompt)


    try:

        result = response.content
        print(result)

        with open(report_path, "w") as f:
            f.write(result)

        return result

    except Exception as e:

        print(e)