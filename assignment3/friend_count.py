import MapReduce
import sys

"""
Counts friend in socaial network (person, friend) in a Simple Python MapReduce Framework
"""

mr = MapReduce.MapReduce()


def mapper(record):
    # key: person
    # value: friend
    key = record[0]
    friend = record[1]
    mr.emit_intermediate(key, friend)

def reducer(key, listOfValues):
    # key: person
    # value: friend list ID
    total = 0
    for friend in listOfValues:
        total += 1
    mr.emit((key,total))
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
