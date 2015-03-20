import MapReduce
import sys

"""
Counts friend in socaial network (person, friend) in a Simple Python MapReduce Framework
"""

mr = MapReduce.MapReduce()


def mapper(record):
    # key:
    # empty
    key = record[1][:-10]
    value = 1
    mr.emit_intermediate(key, value)

def reducer(key, listOfValues):
    # key: ""
    # value: unique trimmed DNA string
    mr.emit(key)
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
