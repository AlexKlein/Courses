import os
import re

import pandas as pd


def find_text_file():
    for path, dirs, files in os.walk(os.getcwd()):
        for f in files:
            if path.find('data_sets') > 0:
                if f.find('.csv') > 0:
                    data_set = read_file(os.path.join(path, f))
                    convert_to_xls(data_set, f.replace(".csv", '.xlsx'))


def read_file(full_path):
    # file = open(full_path, 'r')
    headers = str()
    i = 0
    pattern_start = r'[^*]+(Winter|Summer)*\W\d{4}\W(Winter|Summer)*\W\w+\W\w+'
    pattern_end = r'\w+\W\w+\W\w+$'
    with open(full_path, 'r') as file:
        for line in file:
            i += 1
            if i == 50001:
                break
            line = line.\
                replace('п»ї','').\
                replace('\n', '').\
                replace('-,', ''). \
                replace(', -', ''). \
                replace('"', '')
            if len(headers) == 0:
                line = line.split(',')
                headers = line
                data_set = pd.DataFrame(columns=headers)
            else:
                try:
                    line_start = re.search(pattern_start, line).group(0)
                    line_end = re.search(pattern_end, line).group(0)
                    line = line_start + ',' + line_end

                    series = line.split(',')
                    data_set = data_set.append(pd.Series(series, index=headers), ignore_index=True)
                except:
                    print(line, series, sep='  |||  ')
                    continue

    return data_set


def convert_to_xls(data_set, file_name):
    file_name = file_name.replace('.csv', '.xlsx')
    data_set.to_excel(file_name)


if __name__ == '__main__':
    find_text_file()
