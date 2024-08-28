from crewai import Crew
from vulnerability_guardrail.backend.vul_guard_tasks import *
from vulnerability_guardrail.backend.vul_guard_agents import *

from langchain_openai import ChatOpenAI
import os


with open(r'D:\PycharmProj\science_digital\ini_file\OpenAI\openaikey.txt', 'r') as file_r:
    key = file_r.readline()
os.environ["OPENAI_API_KEY"] = key


class VulnerabilityGuardrail(Crew):

    @staticmethod
    def run(package: str, version: str) -> str:
        vul_guard_agent = vulnerability_guardrail_agent(
            llm=ChatOpenAI(
                model_name="gpt-4o",
                seed=42,
                top_p=0.1,
            )
        )
        vul_guard_task = report_vulnerability_information(vul_guard_agent, package, version)

        crew = Crew(
            agents=[vul_guard_agent],
            tasks=[vul_guard_task],
            verbose=True,
        )
        result = crew.kickoff()
        return str(result)


if __name__ == '__main__':
    query = input("Enter your input with format \"package version\": ")
    package = query.split(" ")[0]
    version = query.split(" ")[1]
    result = VulnerabilityGuardrail.run(package, version)
    print(result)