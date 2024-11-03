from crewai import Task


def report_quality_information(agent):
    return Task(
        description="Given the Python package '{package}' with version '{version}', generate a clear and "
                    "comprehensive report on its software supply chain quality regarding to vulnerabilities, "
                    "tailored for scientists who may not be well-versed in security.\n"
                    "!!!Note:\n"
                    "1. Begin with an overall summary of the software supply chain quality regarding to "
                    "vulnerabilities, followed by detailed descriptions for each dependency in separate paragraphs. "
                    "Finally, give a conclusion about all paragraphs.\n"
                    "2. The report should contain relevant information as much as possible "
                    "for all vulnerable package dependencies identified.\n"
                    "3. In each paragraph, write the hazard that CVE can lead to the scientist, "
                    "considering how exploitation can be triggered and covering key factors such as: "
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
                    "vulnerability can be ignored.\n"
                    "4. Your users are scientists from different domains that may not be familiar about "
                    "software security, so the generated content should be embellished to make it easy to understand "
                    "and scientists needs-and-scenario-considered."
                    "An example paragraph can be:"
                    " - **CVE-ID**: This issue involves the use of ... (CWE-ID). It can lead to "
                    "information disclosure. It can be triggered from a network but requires user interaction, "
                    "with high complexity, and no special privileges required. The attack can be ... "
                    "The complexity of the attack is... The potential impacts are... \n"
                    " - **Hazard to Scientists**: If your software is ... For instance, if ... The attacker can ... "
                    "If your software is not connected to "
                    "a network, or does not require user interaction, or handles public data where leakage is not "
                    "a concern, this risk may be less critical. Otherwise, scientists should be cautious if their "
                    "work involves sensitive data that could be exposed through insecure cryptographic methods. \n"
                    "- **Potential Mitigation**: A potential mitigation can be ...\n"
                    "5. You MUST DO NOT directly list the CVSS metrics with their values in paragraph. "
                    "Those metrics just help to analyse the vulnerability trigger "
                    "and mitigation. Write a easy-reading paragraph to user.\n"
                    "6. You CAN ONLY generate the new report based on existing given content, you MUST NOT make up "
                    "non-existing content or give inaccurate assembled content. ",
        agent=agent,
        expected_output='A report showing software supply chain quality information regarding to vulnerabilities of '
                        'each package.',
    )


def combine_quality_information(agent):
    return Task(
        description="Given a list of code quality reports regarding to software supply chain: {list_of_reports}, "
                    "for a specific science product, "
                    "combine them together as an overall clear and comprehensive new code quality "
                    "report of software supply chain for this science product tailored for scientists "
                    "who may not be well-versed in security.\n"
                    "!!!Note:\n"
                    "1. The list of code quality reports is for dependency libraries for "
                    "the science product. Begin with an overall summary of the code quality issues, "
                    "i.e., 'For this science product, the potential software supply chain hazard includes...', "
                    "followed by detailed descriptions for each dependency library in separate paragraphs. "
                    "Then, give a conclusion about the situation of software supply chain hazard of "
                    "this science product about the content of all paragraphs.\n"
                    "2. Only report dependency information with code quality issues, and remove those without "
                    "hazard.\n"
                    "3. Your users are scientists from different domains that may not be familiar about "
                    "software issues, so the generated content should be embellished to make it easy to understand "
                    "and scientists needs-and-scenario-considered.",
        agent=agent,
        expected_output='A combined report showing overall code quality information for software supply chain.'
    )


def generate_code_fixing_prompt(agent, context_task):
    return Task(
        description="Given a code quality report regarding to software supply chain, you need to "
                    "generate a list of CoT prompt for following code quality repair LLM agent to fix the software "
                    "supply chain hazard. "
                    "Note:\n"
                    "1. Each prompt should start with 'You are a code quality repair agent to fix the hazard in "
                    "software dependencies. You ...', then give the mitigation suggestions.\n"
                    "2. At the final prompt, ask the LLM to generate a new requirement.txt for python program.",
        agent=agent,
        expected_output='A list of CoT prompts to following LLM agent for code quality fixing.',
        context=[context_task]
    )
