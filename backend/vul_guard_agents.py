from crewai import Agent
from vul_guard_tools import *


def vulnerability_guardrail_agent():
    return Agent(
        role="Vulnerability Guardrail that reports the software supply chain vulnerability information for specific "
             "version of the specific python package to the user.",
        goal="Given a python package name with version, you need to firstly fetch CVE & CWE information of this "
             "package and all its dependencies from Google OSI, then clearly report the software supply chain "
             "vulnerability information to the user.",
        backstory="You can only report based on the returns from Google OSI database. "
                  "All the tools provided are to fetch software supply chain vulnerability data from Google OSI "
                  "database. ",
        verbose=True,
        tools=[fetch_vulnerability_information_including_dependency]
    )