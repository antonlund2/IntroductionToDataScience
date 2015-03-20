import MapReduce
import sys

"""
Inverted index in a Simple Python MapReduce Framework
"""

mr = MapReduce.MapReduce()


def mapper(record):
    # key: each word
    # value: document identifer
    text = record[1]
    value = record[0]
    keys = text.split()
    for key in keys:
      mr.emit_intermediate(key, value)

def reducer(key, listOfValues):
    # key: word
    # value: document list ID (unique)
    mr.emit((key,list(set(listOfValues))))
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
