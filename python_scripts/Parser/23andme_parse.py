import os.path
import re

rsID_pattern = re.compile(r'^(rs\d*)\s')

filename = "invalid01.txt"
result = []
tt_and_me = False

def ourfileformat(l):
    res = l.split('\t')
    if res.__len__() != 2 or not res[0].__contains__('rs'):
        return False

    res[1] = res[1].strip()
    if len(res[1]) > 2:
        return False

    return True

## check if file exists
if not os.path.exists(filename):
    print(f"The file {filename} does not exist.")
    exit(1)

## open file to read
with open(filename, mode='r', newline='', encoding='utf-8') as file:

    ## check if 23andMe or normal
    for i, line in enumerate(file):
        if i == 0 and line.__contains__('#'):
            tt_and_me = True

        ## if 23andMe file
        if tt_and_me:
            match_rsId = rsID_pattern.match(line)

            x = line.split('\t')
            if match_rsId is not None:
                if x.__len__() == 4:
                    x[3] = x[3].strip()
                    if x[3] != '--':
                        result.append([x[0], x[3]])

        ## if our format .txt file
        elif ourfileformat(line):
            rsId, expr = line.split('\t')
            expr = expr.strip()
            result.append([rsId, expr])

        ## if not a valid format
        else:
            ## if it´s just an empty line (maybe in-between valid ones), don´t acknowledge
            line = line.strip()
            if line.__len__() == 0:
                continue
            else:
                print("ERROR: file format error")
                result.clear()
                break

## file started with # but was not actually a valid 23andme file
if result.__len__() == 0 and tt_and_me:
    print("ERROR: file format error")

print(result)