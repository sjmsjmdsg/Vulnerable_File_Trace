import requests


def get_vulnerabilities_osv(vul_id):
    """
    Get vulnerability info from OSV
    :param vul_id: vulnerability id
    :return: json of OVS vul info
    """
    url = f"https://api.osv.dev/v1/vulns/{vul_id}"
    response = requests.get(url)
    if response.status_code == 200:
        vulnerabilities = response.json()
        return vulnerabilities
    else:
        return None
