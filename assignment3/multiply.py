import MapReduce
import sys

"""
Matrixm multiplication  of a 5x5 matrix
in a Simple Python MapReduce Framework

"""

mr = MapReduce.MapReduce()



def mapper(record):
    # key:
    # value:
    type = record[0]
    if type == "a":
        mapAMatrix(record)
    else:
        mapBMatrix(record)

def mapAMatrix(record):
    #map row
    for i in range(5):
        key = str(record[1]) + str(i)
        value = (record[2], record[3])
        mr.emit_intermediate(key,value)


def mapBMatrix(record):
    #map column
    #map row
    for i in range(5):
        key = str(i)  + str(record[2])
        value = (record[1], record[3])
        mr.emit_intermediate(key,value)


def reducer(key, listOfValues):
    # key:
    # value:
    #print key
    #print listOfValues
    total = 0
    for i in range(5):
        temp = [v[1] for v in listOfValues if v[0] == i]
        if len(temp) == 2:
            total += temp[0] * temp[1]
    newKey = reformatKey(key)
    mr.emit((newKey[0],newKey[1], total))


def reformatKey(key):
    return [int(key[0]), int(key[1])]

if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
