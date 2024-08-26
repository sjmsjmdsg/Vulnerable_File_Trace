from crewai import Task


def report_vulnerability_information(agent, package, version):
    return Task(
        description=f"Given python package {package} with version {version}, report its software supply chain "
                    f"vulnerability information clearly and pellucidly to user without knowing too much about security."
                    f"!!!Note: "
                    f"1. The report should contain all CVE & CWE information of all package dependencies "
                    f"fetched."
                    f"2. The user may not be familiar about software security, so the generated report should be "
                    f"easy to understand.",
        agent=agent,
        expected_output=f'A report showing software supply chain vulnerability information of {package} {version}.',
    )