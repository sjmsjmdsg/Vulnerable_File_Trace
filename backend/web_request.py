import requests


def get_osv_info(vul_id):
    """
    Get software info from OSV
    :param vul_id: vulnerability id
    :return: json of OSV info
    """
    url = f"https://api.osv.dev/v1/vulns/{vul_id}"
    response = requests.get(url)
    if response.status_code == 200:
        vulnerabilities = response.json()
        return vulnerabilities
    else:
        return None
