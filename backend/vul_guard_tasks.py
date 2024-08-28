from crewai import Task


def report_vulnerability_information(agent, package, version):
    return Task(
        description=f"Given the Python package '{package}' with version '{version}', generate a clear and "
                    f"comprehensive report on its software supply chain vulnerabilities, "
                    f"tailored for scientists who may not be well-versed in security."
                    f"!!!Note: "
                    f"1. Begin with an overall summary of the software supply chain vulnerabilities, followed by "
                    f"detailed descriptions for each dependency in separate paragraphs. Finally, give a conclusion "
                    f"about all paragraphs."
                    f"2. The report should contain vulnerability information as much as possible "
                    f"for all vulnerable package dependencies identified."
                    f"3. In each paragraph, write the hazard that CVE can lead to the scientist, "
                    f"considering how vulnerabilities can be triggered and covering key factors such as: "
                    f"- access (whether network is needed to attack)\n "
                    f"- interaction (whether user interaction is needed to exploit)\n "
                    f"- attack complexity\n "
                    f"- authentication (whether attack can only be done by user with specific privileges)\n "
                    f"- impact confidence (data leakage)\n "
                    f"- impact integer (data integrity damage)\n "
                    f"- impact available (risk of system crashes)\n "
                    f"Given that the software used by the "
                    f"scientists may not be published or put online, or may not need interaction, or handle public "
                    f"data so leakage is ok, or have built-in recovery mechanisms, etc. You should give the situation "
                    f"that under which condition the vulnerability should be cared and under which condition the "
                    f"vulnerability can be ignored."
                    f"4. Your users are scientists from different domains that may not be familiar about "
                    f"software security, so the generated content should be embellished to make it easy to understand "
                    f"and scientists needs-and-scenario-considered."
                    f"An example paragraph can be:"
                    f" - **CVE-XXX-XXX**: This vulnerability involves the use of ... (CWE-XX). It can lead to "
                    f"information disclosure. It can be triggered from a network but requires user interaction, "
                    f"with high complexity, and no special privileges required. If your software is not connected to "
                    f"a network, or does not require user interaction, or handles public data where leakage is not "
                    f"a concern, this risk may be less critical. Otherwise, scientists should be cautious if their "
                    f"work involves sensitive data that could be exposed through insecure cryptographic methods. ",
        agent=agent,
        expected_output=f'A report showing software supply chain vulnerability information of {package} {version}.',
    )