from crewai import Crew
from code_quality_agent.backend.code_quality_tasks import *
from code_quality_agent.backend.code_quality_agents import *

from langchain_openai import ChatOpenAI
import asyncio
import os
root = os.path.dirname(__file__)


class CodeQualityAgent:
    """
    Agent to check the quality issue of the code, including software supply chain risks.
    """
    @staticmethod
    def run(package_version_list: list, verbose: bool):
        """
        Implement main logic by CrewAI. Given software dependencies, generate code quality report and the prompts
        used for succeeding quality issue fixing LLM.
        :param package_version_list: list of software dependencies
        :param verbose: if print intermediate details
        :return: json format results
        """
        # define agent, task and crew
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
            verbose=verbose,
        )

        # asynchronously check the package
        result_list = []
        async_results = asyncio.run(quality_crew.kickoff_for_each_async(inputs=crew_inputs))
        for async_result in async_results:
            result_list.append(str(async_result))

        # combine the results into one report, and generate prompts
        quality_report_agent = code_quality_report_combination_agent(
            llm=ChatOpenAI(
                model_name="gpt-4o",
                seed=42,
                top_p=0.1,
            )
        )
        quality_report_task = combine_quality_information(quality_report_agent)

        prompt_generation_agent = code_fixing_prompt_agent(
            llm=ChatOpenAI(
                model_name="gpt-4o",
                seed=42,
                top_p=0.1,
            )
        )
        prompt_generation_task = generate_code_fixing_prompt(prompt_generation_agent, quality_report_task)
        quality_report_crew = Crew(
            agents=[quality_report_agent, prompt_generation_agent],
            tasks=[quality_report_task, prompt_generation_task],
            verbose=verbose,
        )
        result = quality_report_crew.kickoff(inputs={"list_of_reports": result_list})
        return result


def check_code_quality(openai_key, requirement_path, verbose=False):
    """
    Get the code quality report and the prompts used for succeeding quality issue fixing LLM
    :param openai_key: openai key
    :param requirement_path: file path of the requirements.txt
    :param verbose: if print intermediate details
    :return: json format results
    """
    os.environ["OPENAI_API_KEY"] = openai_key

    with open(requirement_path, 'r', encoding='utf-8') as file_r:
        requirement = [[one_line.strip('\r\n')] for one_line in file_r]
        requirement = [(one_line[0].split('==')[0].lower(), one_line[0].split('==')[1].lower())for one_line in requirement]
        result = CodeQualityAgent.run(requirement, verbose)
        print(result)

        # save file to output path


def main():
    with open(f'{root}/../ini_file/OpenAI/openaikey.txt', 'r') as file_r:
        # prepare input path
        key = file_r.readline()
        requirement_file = f'{root}/data_process/input/requirement.txt'
        verbose = False

        # check requirement.txt
        check_code_quality(requirement_path=requirement_file, openai_key=key, verbose=verbose)


if __name__ == '__main__':
    main()
