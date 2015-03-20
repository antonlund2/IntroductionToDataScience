import MapReduce
import sys

"""
Counts friend in socaial network (person, friend) in a Simple Python MapReduce Framework
"""

mr = MapReduce.MapReduce()


def mapper(record):
    # key: [personA, personB] (sorted)
    # value: [personA, personB]
    sortedRecord = sorted(record)
    key = sortedRecord[0] + sortedRecord[1]
    value = record
    mr.emit_intermediate(key, value)

def reducer(key, listOfValues):
    # key: person
    # value: friend list ID

    #Only list asymmetric relations (there is only 1)
    if len(listOfValues) == 1:
        relation = listOfValues.pop(0)
        mr.emit((relation[0],relation[1]))
        mr.emit((relation[1],relation[0]))
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
