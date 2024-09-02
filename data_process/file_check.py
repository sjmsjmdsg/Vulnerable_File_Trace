from DataLoader import *


def check_processed_files():
    cve_info: dict = DataLoader().load_pickle('/output/cve_dict.pkl')

    cve = {k: v for k, v in cve_info.items() if k.split('-')[1] == '2024'}
    print(1)


def check_multifaceted():
    multifaceted_info: dict = DataLoader().load_pickle('/output/multifaceted_dict.pkl')

    remedy = set()
    for k, v in multifaceted_info.items():
        if len(v['remedy']) > 0:
            remedy.add(v['remedy'])
    print(remedy)


if __name__ == '__main__':
    # check_processed_files()
    check_multifaceted()