from crewai import Crew
from vulnerability_guardrail.backend.vul_guard_tasks import *
from vulnerability_guardrail.backend.vul_guard_agents import *

from langchain_openai import ChatOpenAI
import asyncio
import os
root = os.path.dirname(__file__)

with open(f'{root}/../ini_file/OpenAI/openaikey.txt', 'r') as file_r:
    key = file_r.readline()
os.environ["OPENAI_API_KEY"] = key

ORANGE = "\033[38;5;208m"
GREEN = "\033[92m"
RESET = "\033[0m"


class VulnerabilityGuardrail:

    @staticmethod
    def run(package_version_list: list) -> str:
        vul_guard_agent = vulnerability_guardrail_agent(
            llm=ChatOpenAI(
                model_name="gpt-4o",
                seed=42,
                top_p=0.1,
            )
        )
        vul_guard_task = report_vulnerability_information(vul_guard_agent)

        crew_inputs = []
        for (package, version) in package_version_list:
            crew_inputs.append({'package': package, 'version': version})

        vul_guard_crew = Crew(
            agents=[vul_guard_agent],
            tasks=[vul_guard_task],
            verbose=False,
        )
        # result = vul_guard_crew.kickoff_for_each(inputs=crew_inputs)
        # result_list = str([str(one_result) for one_result in result])
        # print('result1:', result_list)

        result_list = []
        async_results = asyncio.run(vul_guard_crew.kickoff_for_each_async(inputs=crew_inputs))
        for async_result in async_results:
            result_list.append(str(async_result))

        vul_report_agent = vulnerability_report_combination_agent(
            llm=ChatOpenAI(
                model_name="gpt-4o",
                seed=42,
                top_p=0.1,
            )
        )
        vul_report_task = combine_vulnerability_information(vul_report_agent)
        vul_report_crew = Crew(
            agents=[vul_report_agent],
            tasks=[vul_report_task],
            verbose=False,
        )
        result = str(vul_report_crew.kickoff(inputs={"list_of_reports": result_list}))
        return result


def main():
    requirement = DataLoader().load_txt('/input/requirement.txt')
    requirement = [(one_line[0].split('==')[0].lower(), one_line[0].split('==')[1].lower())for one_line in requirement]
    result = VulnerabilityGuardrail.run(requirement)
    print(result.replace("<ORANGE>", ORANGE).replace("<GREEN>", GREEN).replace("<END>", RESET))


if __name__ == '__main__':
    # run checking single package version
    # query = input("Enter your input with format \"package version\": ")
    # package = query.split(" ")[0]
    # version = query.split(" ")[1]
    # result = VulnerabilityGuardrail.run(package, version)
    # print(result)

    # check requirement.txt
    main()
