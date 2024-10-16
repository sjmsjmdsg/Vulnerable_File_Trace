from code_quality_agent.data_process.DataLoader import *
import re
import tqdm


def load_nvd_info():
    """
    Load useful info from raw nvd feeds
    :return: {cve_id: {'cvss_metrics': , 'description': , 'cwe_list': }...}
    """
    dir_path = os.path.dirname(__file__) + '/ini_file/nvd/'
    cve_dict = {}
    for sub_dir in tqdm.tqdm(os.listdir(dir_path)):
        whole_sub_dir = dir_path + sub_dir + '/'
        for one_file in os.listdir(whole_sub_dir):
            file_r = DataLoader().load_json('/ini_file/nvd/' + sub_dir + '/' + one_file)
            for one_cve in file_r['CVE_Items']:
                _id = one_cve['cve']['CVE_data_meta']['ID']
                if _id == "CVE-2021-41495":
                    print(1)
                desc = one_cve['cve']['description']['description_data'][0]['value']
                if re.search(r'\*\* REJECT \*\*|\*\* DISPUTED \*\*', desc):
                    continue

                # Collect CWE ids
                problem_data = one_cve['cve']['problemtype']['problemtype_data']
                cwe_list = []
                for one_ele in problem_data:
                    if one_ele.get('value') is not None and one_ele['value'] != 'NVD-CWE-Other':
                        cwe_list.append(one_ele['value'])
                    elif one_ele.get('description') is not None:
                        for sub_ele in one_ele['description']:
                            if sub_ele['value'] != 'NVD-CWE-Other':
                                cwe_list.append(sub_ele['value'])
                    else:
                        print(one_cve)

                # Collect CVSS info
                cvss_dict = one_cve['impact']
                if cvss_dict.get('baseMetricV3') is not None:
                    cvss_dict = cvss_dict['baseMetricV3']
                elif cvss_dict.get('baseMetricV2') is not None:
                    cvss_dict = cvss_dict['baseMetricV2']
                else:
                    print(cvss_dict)

                cve_dict[_id] = {'cvss_metrics': cvss_dict, 'description': desc, 'cwe_list': cwe_list}
    DataWriter('/output/cve_dict.pkl').write_pickle(cve_dict)


def load_cwe_info():
    """
    Load useful info from raw cwe feeds
    :return: {cwe_id: {'cwe': , 'description': , 'description_extension': }...}
    """
    cwe_list = [DataLoader().load_csv('/ini_file/cwe/1000.csv', ignore_header=True),
                DataLoader().load_csv('/ini_file/cwe/1194.csv', ignore_header=True),
                DataLoader().load_csv('/ini_file/cwe/699.csv', ignore_header=True)]
    cwe_dict = {}

    for one_cwe in cwe_list:
        for one_line in one_cwe:
            _id = one_line[0]
            name = one_line[1]
            desc = one_line[4]
            desc_ext = one_line[5]

            # Add prefix CWE
            cwe_dict['CWE-' + _id] = {'cwe': name, 'description': desc, 'description_extension': desc_ext}

    DataWriter('/output/cwe_dict.pkl').write_pickle(cwe_dict)


def process_multifaceted_info():
    """
    Transfer old multifaceted data into tool-usable data
    :return: {cve_id: {key: value, ...}, ...}
    """
    file_r = DataLoader().load_csv('/ini_file/multifaceted/PycharmProjmultifacetedmultifacetedcveinfo.csv')

    trans_dict = {}
    for one_line in tqdm.tqdm(file_r):
        for i in range(4, 9):
            one_line[i] = re.sub(r'\([^)]*\)$', '', one_line[i])
        trans_dict[one_line[0]] = {'vulnerability type': one_line[4],
                                   'root cause': one_line[6], 'attack vector': one_line[7], 'impact': one_line[8],
                                   'remedy': one_line[10]}
        if one_line[-1] != '':
            trans_dict[one_line[0]]['exploit method'] = 'existed'
        else:
            trans_dict[one_line[0]]['exploit method'] = 'not found'

    DataWriter('/output/multifaceted_dict.pkl').write_pickle(trans_dict)
    print(1)


if __name__ == '__main__':
    # load_nvd_info()
    # load_cwe_info()

    process_multifaceted_info()