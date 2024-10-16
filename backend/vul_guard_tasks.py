from crewai import Task


def report_quality_information(agent):
    return Task(
        description="Given the Python package '{package}' with version '{version}', generate a clear and "
                    "comprehensive report on its software supply chain vulnerabilities, "
                    "tailored for scientists who may not be well-versed in security."
                    "!!!Note: "
                    "1. Begin with an overall summary of the software supply chain vulnerabilities, followed by "
                    "detailed descriptions for each dependency in separate paragraphs. Finally, give a conclusion "
                    "about all paragraphs."
                    "2. The report should contain vulnerability information as much as possible "
                    "for all vulnerable package dependencies identified."
                    "3. In each paragraph, write the hazard that CVE can lead to the scientist, "
                    "considering how vulnerabilities can be triggered and covering key factors such as: "
                    "attackVector (accessVector): whether network is needed to attack, "
                    "userInteraction (userInteractionRequired): whether user interaction is needed to exploit, "
                    "attackComplexity (accessComplexity), "
                    "privilegesRequired (authentication): whether attack can only be done by user with specific "
                    "privileges, "
                    "confidentialityImpact: data leakage, "
                    "integrityImpact: data integrity damage, "
                    "availabilityImpact: risk of system crashes. "
                    "If the remedy is not empty, give the potential mitigation method. "
                    "Given that the software used by the "
                    "scientists may not be published or put online, or may not need interaction, or handle public "
                    "data so leakage is ok, or have built-in recovery mechanisms, etc. You should give the situation "
                    "that under which condition the vulnerability should be cared and under which condition the "
                    "vulnerability can be ignored."
                    "4. Your users are scientists from different domains that may not be familiar about "
                    "software security, so the generated content should be embellished to make it easy to understand "
                    "and scientists needs-and-scenario-considered."
                    "An example paragraph can be:"
                    " - **CVE-ID**: This vulnerability involves the use of ... (CWE-ID). It can lead to "
                    "information disclosure. It can be triggered from a network but requires user interaction, "
                    "with high complexity, and no special privileges required. The attack can be ... "
                    "The complexity of the attack is... The potential impacts are... \n"
                    " - **Hazard to Scientists**: If your software is ... For instance, if ... The attacker can ... "
                    "If your software is not connected to "
                    "a network, or does not require user interaction, or handles public data where leakage is not "
                    "a concern, this risk may be less critical. Otherwise, scientists should be cautious if their "
                    "work involves sensitive data that could be exposed through insecure cryptographic methods. \n"
                    "- **Potential Mitigation**: A potential mitigation can be ... "
                    "5. You MUST DO NOT directly list the CVSS metrics with their values in paragraph. "
                    "Those metrics just help to analyse the vulnerability trigger "
                    "and mitigation. Write a easy-reading paragraph to user."
                    "6. You CAN ONLY generate the new report based on existing given content, you MUST NOT make up "
                    "non-existing content or give inaccurate assembled content. ",
        agent=agent,
        expected_output='A report showing software supply chain vulnerability information of each package.',
    )


def combine_quality_information(agent):
    return Task(
        description="Given a list of software supply chain vulnerability reports {list_of_reports} for a specific "
                    "science product, "
                    "1) combine them together as an overall clear and comprehensive new software supply chain "
                    "vulnerability report for this science product tailored for scientists "
                    "who may not be well-versed in security; 2) generate a prompt for following vulnerability "
                    "repair LLM agent to fix the hazard."
                    "!!!Note:\n"
                    "1. The list of software supply chain vulnerability reports is for dependency libraries for "
                    "the science product. Begin with an overall summary of the software supply chain vulnerabilities, "
                    "i.e., 'For this science product, the potential software supply chain hazard includes...', "
                    "followed by detailed descriptions for each dependency library in separate paragraphs. "
                    "Then, give a conclusion about the situation of software supply hain vulnerability hazard of "
                    "this science product about the content of all paragraphs. "
                    "Finally, generate a prompt for following vulnerability repair LLM agent to fix the hazard. "
                    "The prompt should start with 'You are a vulnerability repair agent to fix the hazard in software "
                    "dependencies. You ...', then combine the mitigation suggestions, and ask the LLM to generate a "
                    "new requirement.txt for python program. \n"
                    "2. Only report vulnerable dependency information, and remove those without vulnerability "
                    "hazard.\n"
                    "3. Your users are scientists from different domains that may not be familiar about "
                    "software security, so the generated content should be embellished to make it easy to understand "
                    "and scientists needs-and-scenario-considered."
                    "4. Label vulnerability trigger information, i.e., 'If your software does not interact with web "
                    "content or is used in a controlled, offline environment, the risk may be less critical. "
                    "However,...' into orange, mitigation information into green, and agent prompt information into "
                    "pink using tags <COLOR>...<END>, i.e., "
                    "<ORANGE>some content<END>,  <GREEN>some content<END>, and <PINK>some content<END>. "
                    "Remember to add <END> at end of the agent prompt.",
        agent=agent,
        expected_output='A combined report showing overall software supply chain vulnerability information and the '
                        'prompt to following LLM agent for vulnerability fixing.'
    )
