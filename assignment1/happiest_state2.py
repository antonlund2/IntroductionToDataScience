import sys
import json
from xml.dom import minidom

def constructStatesDictionary():
   states = {
        'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AS': 'American Samoa',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District of Columbia',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'GU': 'Guam',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MP': 'Northern Mariana Islands',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NA': 'National',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'PR': 'Puerto Rico',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VI': 'Virgin Islands',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming'
   }
   statesDict={}

   keys=['name','coordinates','score']
   for ab, state in states.iteritems():
       statesDict[ab]=dict(zip(keys,[state,[0,0],0]))
   return statesDict

def insertPolygonpathstoStatesDict(statesDict):
    stateslist = parseStatesXml(statesDict)
    return statesDict

def parseStatesXml(statesDict):
    xmldoc = minidom.parse('states.xml')
    stateslist = xmldoc.getElementsByTagName('state')
    for state in stateslist:
        pathlist = []
        name = state.attributes['name'].value
        pointlist = state.getElementsByTagName('point')
        #Put coordinates into list
        for point in pointlist:
            lat =  float(point.attributes['lat'].value.encode('utf-8'))
            lng =  float(point.attributes['lng'].value.encode('utf-8'))
            pathlist.append([lat,lng])
        #Find centre of each polygon
        longlist = [row[0] for row in pathlist]
        long = sum(longlist)/len(longlist)
        latlist = [row[1] for row in pathlist]
        lat = sum(latlist)/len(latlist)
        print "'" + name + "' : " + "'[" +str(long) +"," + str(lat) + "]'"
        #Create pathobject and put into statesDict
        for key in statesDict:
            if statesDict[key]['name'] == name:
                statesDict[key]['coordinates'] = [long,lat]
                break
    return statesDict



def constructDictionary():
    afinnfile = open(sys.argv[1]) # Reads file for dictionary
    scores = {} # Iniatialize an empty dictionary
    for line in afinnfile:
        term, score = line.split("\t") # file is tab-delimited
        scores[term] = int(score)
    return scores

def parseTweetFile():
    tweetFile = open(sys.argv[2])
    tweets = []
    keys = ['text','score','coordinates']
    for line in tweetFile:
        tweet = json.loads(line)
        if "coordinates" in tweet and tweet['place'] is not None:
            text = getText(tweet)
            coordinates = getCoordinates(tweet['place'])
            tweets.append(dict(zip(keys,[text,0,coordinates])))
    return tweets

def getText(tweet):
    if "text" in tweet:
        return tweet['text']
    else:
        return ""

def getCoordinates(place):
    coordinatesBox =  place['bounding_box']['coordinates'][0]
    longlist = [row[0] for row in coordinatesBox]
    long = sum(longlist)/len(longlist)
    latlist = [row[1] for row in coordinatesBox]
    lat = sum(latlist)/len(latlist)
    return [lat,long]

def calculateTweetScores(tweets, scores):
    for tweet in tweets:
        score = 0
        words = tweet['text'].split(" ")
        for word in words:
            if word in scores:
                score += scores[word]
        tweet['score']=score
    return tweets


def calculateStateScores(statesDict, tweets):
    for tweet in tweets:
        state = getClosestState(statesDict,tweet)
        if state != "":
            #print state
            #print statesDict[state]['coordinates']
            #print tweet['coordinates']
            statesDict[state]['score'] += tweet['score']
    return statesDict

def getClosestState(statesDict, tweet):
    minDist = 100
    closestState = ""
    for state in statesDict:
        if statesDict[state]['coordinates'] != [0,0]:
            dist = calculateDistance(tweet['coordinates'],statesDict[state]['coordinates'])
            if dist < minDist:
                minDist = dist
                closestState = state
    #If distance is over a certain limit, dont add
    if minDist < 3:
        return closestState
    else:
        return ""

def calculateDistance(coord1, coord2):
    return ( (coord1[0]-coord2[0]) ** 2 + (coord1[1] - coord2[1]) ** 2) ** (0.5)




def printHappiestState(statesDict):

    state = max(statesDict.keys(), key=lambda x: statesDict[x]['score'])
    print state, statesDict[state]['score']

def main():
    # Reading and parsing sentiment information
    termScores = constructDictionary()
    tweets = parseTweetFile()
    tweets = calculateTweetScores(tweets, termScores)

    statesDict = constructStatesDictionary()
    statesDict = insertPolygonpathstoStatesDict(statesDict)
    statesDict = calculateStateScores(statesDict, tweets)

    #printHappiestState(statesDict)
if __name__ == '__main__':
    main()
