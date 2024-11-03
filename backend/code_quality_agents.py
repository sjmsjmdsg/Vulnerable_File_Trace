from crewai import Agent
from code_quality_agent.backend.code_quality_tools import *


def code_quality_agent(llm):
    return Agent(
        role="Code Quality Agent that reports the detailed software supply chain quality information regarding to "
             "vulnerability for specific version of the specific python package to the user.",
        goal="Given a python package name with version, you need to firstly fetch CVE & CWE information of this "
             "package and all its dependencies from Google OSI database, then provide a detailed and clear "
             "software supply chain quality report regarding to vulnerability to the user.\n"
             "You can only report based on the returns from Google OSI database.",
        backstory="All the tools provided are to fetch software supply chain quality data regarding to vulnerability "
                  "from Google OSI database.\n"
                  "Familiarize yourself with key CVSS metrics:\n"
                  "1. attackVector (accessVector): shows whether network is needed to exploitation.\n"
                  "2. attackComplexity (accessComplexity): shows the conditions beyond the attacker's control that "
                  "must exist for exploitation.\n"
                  "3. privilegesRequired (authentication): shows level of privileges an attacker must possess "
                  "before exploiting.\n"
                  "4. userInteraction (userInteractionRequired): shows whether the user participation is required for "
                  "exploitation.\n"
                  "5. confidentialityImpact: means level of access disclosure due to attack.\n"
                  "6. integrityImpact: measures level of data integrity losses due to attack.\n"
                  "7. availabilityImpact: measures whether denial of service will happen due to attacker.",
        allow_delegation=False,
        verbose=False,
        tools=[fetch_vulnerability_information_including_dependency],
        llm=llm
    )


def code_quality_report_combination_agent(llm):
    return Agent(
        role="A report combination agent to combine different code quality reports and paragraphs regarding to "
             "software supply chain into one overall reports.",
        goal="Given several code quality reports regarding to software supply chain for a specific science "
             "product, which involves several paragraphs, "
             "you need to combine them into an overall report for this science product with several paragraphs.\n"
             "You have to combine the "
             "overlapping contents together, remove duplicated contents, and finally provide a detailed and clear "
             "overall code quality report to the user.",
        backstory="You CAN ONLY generate the new report based on existing given content, you MUST NOT make up "
             "non-existing content or give inaccurate assembled content. ",
        allow_delegation=False,
        verbose=False,
        llm=llm
    )


def code_fixing_prompt_agent(llm):
    return Agent(
        role="A prompt generation agent aiming at generating prompt for succeeding LLM to optimise code quality "
             "issue.",
        goal="Given a code quality issue report, you need to generate a prompt for other LLM to fix the code issues. "
             "The prompt should consider all the issues in the report, so the succeeding LLM can know the full "
             "context. The prompt should be clear and effective.",
        backstory="Chain-of-Thought (CoT) is considered effective in complex tasks. Based on the requirements, you "
                  "need to generate a single prompt or a list of CoT prompt for succeeding LLMs to fix issues.",
        allow_delegation=False,
        verbose=False,
        llm=llm
    )
