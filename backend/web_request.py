import requests


def get_osv_info(adv_id):
    """
    Get software advisory info from OSV
    :param adv_id: advisory entry id
    :return: json of OSV advisory info
    """
    url = f"https://api.osv.dev/v1/vulns/{adv_id}"
    response = requests.get(url)
    if response.status_code == 200:
        adv_info = response.json()
        return adv_info
    else:
        return None
