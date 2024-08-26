import os
import csv
import pickle
import json


class DataLoader:
    def __init__(self):
        self.root = os.path.dirname(__file__)

    def load_csv(self, file_path,  delimiter=',', ignore_header=False, encoding='utf-8'):
        with open(self.root + file_path, encoding=encoding) as file_r:
            file_r = csv.reader(file_r, delimiter=delimiter)
            if ignore_header:
                next(file_r, None)
            csv_file = []
            for one_line in file_r:
                csv_file.append(one_line)
            return csv_file

    def load_pickle(self, file_path, self_path=False):
        if not self_path:
            with open(self.root + file_path, 'rb') as file_r:
                file_r = pickle.load(file_r)
                return file_r
        else:
            with open(file_path, 'rb') as file_r:
                file_r = pickle.load(file_r)
                return file_r

    def load_txt(self, file_path, encoding='utf-8'):
        with open(self.root + file_path, 'r', encoding=encoding) as file_r:
            return [[one_line.strip('\r\n')] for one_line in file_r]

    def load_json(self, file_path):
        with open(self.root + file_path, 'r', encoding='utf-8') as file_r:
            return json.load(file_r)


class DataWriter:
    def __init__(self, input_path):
        self.file_path = os.path.dirname(__file__) + input_path

    def write_csv(self, file_write, delimiter=','):
        with open(self.file_path, 'w', encoding='utf-8', newline='') as file_w:
            file_w = csv.writer(file_w, delimiter=delimiter, quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for one_line in file_write:
                file_w.writerow(one_line)

    def write_pickle(self, write_pkl):
        with open(self.file_path, 'wb') as file_w:
            pickle.dump(write_pkl, file_w)
            file_w.flush()

    def write_txt(self, write_file):
        with open(self.file_path, 'w', encoding='utf-8') as file_w:
            for one_line in write_file:
                if len(one_line) == 1:
                    file_w.write(one_line[0] + '\n')
                else:
                    file_w.write(' '.join(one_line) + '\n')

    def write_json(self, write_file):
        with open(self.file_path, 'w', encoding='utf-8') as file_w:
            json.dump(write_file, file_w)

