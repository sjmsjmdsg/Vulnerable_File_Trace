from crewai import Task


def report_vulnerability_information(agent, package, version):
    return Task(
        description=f"Given python package {package} with version {version}, report its detailed software supply chain "
                    f"vulnerability information clearly and pellucidly to scientists without knowing too much about "
                    f"security."
                    f"!!!Note: "
                    f"1. You need to firstly give an overall software supply chain vulnerability information, then "
                    f"for each of the dependents, giving the details separately as a paragraph."
                    f"2. The report should contain all CVE & CWE information of all package dependencies "
                    f"fetched."
                    f"3. Your users are scientists from different domains that may not be familiar about "
                    f"software security, so the generated report should be easy to understand."
                    f"4. When giving the information, you should consider the features of scientist work. For example, "
                    f"the software used by the scientist may not be published or put online, so based on the fetched "
                    f"CVE information, you should give the situation that under which condition the vulnerability "
                    f"should be cared and under which condition the vulnerability can be ignored."
                    f"5. When considering the hazard of CVE, you should think based on condition of how vulnerability "
                    f"can be triggered, and features including access (whether network is needed to attack), "
                    f"interaction (whether user interaction is needed to exploit), attack complexity, authentication, "
                    f"impact confidence, impact integer and impact available.",
        agent=agent,
        expected_output=f'A report showing software supply chain vulnerability information of {package} {version}.',
    )