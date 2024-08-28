from crewai import Agent
from vul_guard_tools import *


def vulnerability_guardrail_agent(llm):
    return Agent(
        role="Vulnerability Guardrail that reports the detailed software supply chain vulnerability information for "
             "specific version of the specific python package to the user.",
        goal="Given a python package name with version, you need to firstly fetch CVE & CWE information of this "
             "package and all its dependencies from Google OSI database, then provide a detailed and clear "
             "software supply chain vulnerability report to the user. ",
        backstory="You can only report based on the returns from Google OSI database. \n"
                  "All the tools provided are to fetch software supply chain vulnerability data from Google OSI "
                  "database. \n"
                  "Familiarize yourself with key CVSS metrics"
                  "1. access: shows whether network is needed to exploit the vulnerability."
                  "2. attack complexity: shows the conditions beyond the attacker's control that must exist to exploit "
                  "the vulnerability."
                  "3. authentication: shows level of privileges an attacker must possess before exploiting."
                  "4. interaction: shows whether the user participation is required to exploit the vulnerability."
                  "5. impact confidence: means level of access disclosure due to attack."
                  "6. impact integer: measures level of data integrity losses due to attack."
                  "7. impact available: measures whether denial of service will happen due to attacker.",
        verbose=True,
        tools=[fetch_vulnerability_information_including_dependency],
        llm=llm
    )
