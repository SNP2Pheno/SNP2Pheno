import pandas as pd
import pickle
import sys

## print(sys.argv[1])
## print(sys.argv[2])
## print(sys.argv[3])
## print(sys.argv[4])

def getrsIDsOfModel():
    arg2 = sys.argv[2].split(',')
    rsIds = {}

    for line in arg2:
        l = line.split(':')
        rsIds.update({l[0]: l[1]})

    return rsIds

def readPersonFile(filename):
    ## hardcoded for now
    rsIds = {
        "rs12913832": "GG",
        "rs12896399": "GG",
        "rs1408799": "CC"
    }
    return rsIds

def distinguishVariants():
    var = sys.argv[4].split(';')
    result = {}

    for v in var:
        n = v.split(':')
        n2 = n[1].split(',')
        result.update({n[0]:n2})
    return result

pkl_path = sys.argv[1]
prs_file = sys.argv[3]
Model_rsIds = getrsIDsOfModel()
Person_rsIds = readPersonFile(prs_file)
variants = distinguishVariants()

model = pickle.load(open(pkl_path, 'rb'))

## ALL OUR VARIABLES:
## print(Model_rsIds)
## print(Person_rsIds)
## print(pkl_path)
## print(prs_file)
## print(variants)


## d is a dictionary for all the expressions => do we have the expression in our variants --> 1, if not --> 0

d = {}
inserted = False

for rs in Model_rsIds:
    ## if the user´s rsIDs are in our DB
    if rs in Person_rsIds:
        d[rs] = []

        if Model_rsIds[rs] != "?":

            if type(Person_rsIds[rs]) != str or len(Person_rsIds[rs]) < 2:
                d[rs].append(-1)
            elif Person_rsIds[rs].find(Model_rsIds[rs]) >= 0:
                d[rs].append(1)
            else:
                d[rs].append(0)
        else:
            if type(Person_rsIds[rs]) != str or len(Person_rsIds[rs]) < 2 or Person_rsIds[rs] not in variants['rs12203592']:
                d[rs] = -1
            else:
                d[rs] = variants['rs12203592'].index[Person_rsIds[rs]]

## X = pd.DataFrame(
##    data,
##    columns=obj.feature_names_in_
##)

df = pd.DataFrame.from_dict(d)

print(df['rs12913832'].values)
print(df['rs12896399'].values)
print(df['rs1408799'].values)
print(model.predict(df))

