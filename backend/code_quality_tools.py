from crewai_tools import tool
from open_source_insights_api import os_insights
from data_process.DataLoader import *
from code_quality_agent.backend.web_request import *

import tqdm

# {cve_id: {'cvss_metrics': , 'description': , 'cwe_list': }...}
cve_info: dict = DataLoader().load_pickle('/output/cve_dict.pkl')
# {cwe_id: {'cwe': , 'description': , 'description_extension': }...}
cwe_info: dict = DataLoader().load_pickle('/output/cwe_dict.pkl')
# {cve_id: {key: value, ...}, ...}
multifaceted_info: dict = DataLoader().load_pickle('/output/multifaceted_dict.pkl')


def fetch_vulnerability_information(osi, package_name, version):
    """
    Fetch vulnerability information about a python package with specified version.
    The returns include CVE information list and CWE information list.
    :param osi:
    :param package_name: the target python package name
    :param version: the target package version
    :return:
    """
    pkg = osi.GetVersion('pypi', package_name, version)
    cve_info_collection, cwe_info_collection, multifaceted_info_collection = [], [], []

    if pkg.get('advisoryKeys'):
        cves = set()
        for one_adv in pkg['advisoryKeys']:
            # Fetch CVE info from advisory
            if one_adv['id'][:4] == 'CVE-':
                cves.add(one_adv['id'])
            elif one_adv['id'][:5] == 'GHSA-':
                osv_info = get_osv_info(one_adv['id'])
                if osv_info and osv_info.get('references'):
                    cves = cves.union(set(one_adv['url'].split('/')[-1] for one_adv in osv_info['references']
                                          if one_adv['type'] == 'ADVISORY' and one_adv['url'].split('/')[-1][
                                                                               :4] == 'CVE-'))
            elif one_adv['id'][:4] == 'PSF-':
                osv_info = get_osv_info(one_adv['id'])
                if osv_info and osv_info.get('aliases'):
                    cves = cves.union(set(one_vul for one_vul in osv_info['aliases'] if one_vul[:4] == 'CVE-'))
            elif one_adv['id'][:6] == 'PYSEC-':
                osv_info = get_osv_info(one_adv['id'])
                if osv_info and osv_info.get('related'):
                    cves = cves.union(set(one_adv for one_adv in osv_info['related'] if one_adv[:4] == 'CVE-'))

        cve_info_collection += [{**cve_info[one_cve], 'cve_id': one_cve} for one_cve in cves if
                                cve_info.get(one_cve)]
        cwe_info_collection += [[cwe_info[one_cwe]] for one_info in cve_info_collection
                                for one_cwe in one_info['cwe_list'] if cwe_info.get(one_cwe)]
        multifaceted_info_collection += [multifaceted_info[one_cve] for one_cve in cves if
                                         multifaceted_info.get(one_cve)]

    return cve_info_collection, cwe_info_collection, multifaceted_info_collection


@tool("fetch_vulnerability_information_including_dependency")
def fetch_vulnerability_information_including_dependency(package_name: str, version: str) -> str:
    """
    Fetch vulnerability information about a python package with specified version and all the dependencies.
    The returns include CVE and CWE information of all involved packages.
    :param package_name: the target python package name.
    :param version: the target package version.
    :return: CVE information and CWE information needed in the report.
    """
    osi = os_insights.query()
    cve_info_collection, cwe_info_collection, multifaceted_info_collection = \
        fetch_vulnerability_information(osi, package_name, version)

    if len(cve_info_collection) > 0:
        return_info = (f"For {package_name} {version}, all fetched CVE information: {cve_info_collection}, "
                       f"all fetched detailed CVE information (including vulnerability key aspects collected from "
                       f"multiple sources, detailed CVSS aspects, and exploit availability): "
                       f"{multifaceted_info_collection}, "
                       f"all fetched CWE information corresponding to fetched CVEs: {cwe_info_collection}.")
    else:
        return_info = f"For {package_name} {version}, there is no direct CVE & CWE information."

    deps = osi.GetDependencies('pypi', package_name, version)
    if deps.get('nodes'):
        for one_dep in tqdm.tqdm(deps['nodes']):
            dep_relation = one_dep['relation']
            if dep_relation != 'SELF':
                dep_name, dep_version = one_dep['versionKey']['name'], one_dep['versionKey']['version']
                cve_info_collection, cwe_info_collection, multifaceted_info_collection = \
                    (fetch_vulnerability_information(osi, dep_name, dep_version))

                if len(cve_info_collection) > 0:
                    return_info += (
                        f"\n{package_name} {version} has {dep_relation} dependency {dep_name} {dep_version}, "
                        f"it has CVE information: {cve_info_collection}, "
                        f"its detailed CVE information (including vulnerability key aspects collected from "
                        f"multiple sources, detailed CVSS aspects, and exploit availability): "
                        f"{multifaceted_info_collection}, "
                        f"it has CWE information corresponding to fetched CVEs: {cwe_info_collection},"
                        f"which can lead to supply chain vulnerability risks.")

    return return_info
