import re

rsid_pattern = re.compile(r'^(rs\d*)\s')

filename = "genome_Daiyu_Hurst_Full_20160326092405.txt"
list = []


with open(filename, mode='r', newline='', encoding='utf-8') as file:
    for line in file:
        match_rsId = rsid_pattern.match(line)

        x = line.split('\t')
        if (match_rsId is not None):
            if (x.__len__() > 1):
                # print(x[3])
                # print(x[0])
                x[3] = x[3].strip()
                if (x[3] != '--'):
                    list.append([x[0], x[3]])

print (list)