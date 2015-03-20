import MapReduce
import sys

"""
Relational join in a Simple Python MapReduce Framework
"""

mr = MapReduce.MapReduce()



def mapper(record):
    # key: order ID
    # value: attributes
    key = record[1]
    mr.emit_intermediate(key, record)

def getEndIndex(db):
    if db == "line_item":
        return 17
    else:
        return 10


def reducer(key, listOfValues):
    # key: order ID
    # value: first value is order row and rest its list_item rows

    order = listOfValues.pop(0)
    for list_item in listOfValues:
        #print len([order,list_item])
        mr.emit(order + list_item)


if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
