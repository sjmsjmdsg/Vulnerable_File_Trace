from crewai import Crew
from code_quality_agent.backend.code_quality_tasks import *
from code_quality_agent.backend.code_quality_agents import *

from langchain_openai import ChatOpenAI
import asyncio
import os
root = os.path.dirname(__file__)

with open(f'{root}/../ini_file/OpenAI/openaikey.txt', 'r') as file_r:
    key = file_r.readline()
os.environ["OPENAI_API_KEY"] = key

ORANGE = "\033[38;5;208m"
GREEN = "\033[92m"
PINK = "\033[38;2;255;105;180m"
RESET = "\033[0m"


class CodeQualityAgent:

    @staticmethod
    def run(package_version_list: list) -> str:
        quality_agent = code_quality_agent(
            llm=ChatOpenAI(
                model_name="gpt-4o",
                seed=42,
                top_p=0.1,
            )
        )
        quality_task = report_quality_information(quality_agent)

        crew_inputs = []
        for (package, version) in package_version_list:
            crew_inputs.append({'package': package, 'version': version})

        quality_crew = Crew(
            agents=[quality_agent],
            tasks=[quality_task],
            verbose=False,
        )

        result_list = []
        async_results = asyncio.run(quality_crew.kickoff_for_each_async(inputs=crew_inputs))
        for async_result in async_results:
            result_list.append(str(async_result))

        quality_report_agent = code_quality_report_combination_agent(
            llm=ChatOpenAI(
                model_name="gpt-4o",
                seed=42,
                top_p=0.1,
            )
        )
        quality_report_task = combine_quality_information(quality_report_agent)
        quality_report_crew = Crew(
            agents=[quality_report_agent],
            tasks=[quality_report_task],
            verbose=False,
        )
        result = str(quality_report_crew.kickoff(inputs={"list_of_reports": result_list}))
        return result


def main():
    requirement = DataLoader().load_txt('/input/requirement.txt')
    requirement = [(one_line[0].split('==')[0].lower(), one_line[0].split('==')[1].lower())for one_line in requirement]
    result = CodeQualityAgent.run(requirement)
    print(result.replace("<ORANGE>", ORANGE).replace("<GREEN>", GREEN).replace("<PINK>", PINK)
          .replace("<END>", RESET))


if __name__ == '__main__':
    # run checking single package version
    # query = input("Enter your input with format \"package version\": ")
    # package = query.split(" ")[0]
    # version = query.split(" ")[1]
    # result = CodeQualityAgent.run(package, version)
    # print(result)

    # check requirement.txt
    main()
