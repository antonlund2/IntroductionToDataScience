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

   for state in statesDict:
       coordinates = getCoordinates(statesDict[state]['name'])
       if coordinates != "":
           statesDict[state]['coordinates']=coordinates
   return statesDict

def getCoordinates(state):
    statesCoordinates ={
        'Alaska' : [61.4232930233,-153.637046512],
        'Alabama' : [32.1413047619,-86.698547619],
        'Arkansas' : [34.5301224138,-91.2841706897],
        'Arizona' : [34.4441623529,-114.267925882],
        'California' : [35.1157081081,-117.03099009],
        'Colorado' : [38.59918,-106.24686],
        'Connecticut' : [41.588453125,-72.747946875],
        'Delaware' : [39.2822421053,-75.4688157895],
        'Florida' : [29.4640287356,-83.3713528736],
        'Georgia' : [32.5739875,-82.9491625],
        'Hawaii' : [20.6617733333,-157.063526667],
        'Iowa' : [41.9587152542,-93.1368288136],
        'Idaho' : [45.2892601626,-115.460625203],
        'Illinois' : [39.4357685714,-89.6115142857],
        'Indiana' : [38.4496623529,-87.07058],
        'Kansas' : [39.3514611111,-96.4829222222],
        'Kentucky' : [37.80897,-86.04640125],
        'Louisiana' : [31.0071220183,-92.2249743119],
        'Massachusetts' : [42.165574,-71.611714],
        'Maryland' : [39.0173518182,-77.5998363636],
        'Maine' : [45.4647410714,-69.2607571429],
        'Michigan' : [44.9807491379,-85.3425396552],
        'Minnesota' : [47.3368340909,-93.5194806818],
        'Missouri' : [38.4546507692,-91.4543630769],
        'Mississippi' : [32.8266583333,-90.6849595238],
        'Montana' : [45.746922807,-113.089645614],
        'North Carolina' : [35.476725,-81.1417483333],
        'North Dakota' : [47.7887,-97.8860956522],
        'Nebraska' : [41.9200651163,-97.3551232558],
        'New Hampshire' : [43.9991308411,-71.7222953271],
        'New Jersey' : [40.2838351852,-74.7846703704],
        'New Mexico' : [33.4697666667,-106.976466667],
        'Nevada' : [36.66445625,-115.0815625],
        'New York' : [43.0961849206,-74.9728968254],
        'Ohio' : [39.6671333333,-82.5540071429],
        'Oklahoma' : [34.4158234043,-97.5116723404],
        'Oregon' : [45.1477408,-120.0911144],
        'Pennsylvania' : [41.018734375,-76.062546875],
        'Rhode Island' : [41.6254,-71.469155],
        'South Carolina' : [33.6756596154,-81.5158115385],
        'South Dakota' : [43.6930230769,-97.8647884615],
        'Tennessee' : [35.9475175439,-85.9047491228],
        'Texas' : [30.9858695906,-98.3892070175],
        'Utah' : [39.5701285714,-111.761771429],
        'Virginia' : [37.8903835526,-79.4718105263],
        'Vermont' : [44.0553820755,-72.6349169811],
        'Washington' : [46.5818235772,-121.552456911],
        'Wisconsin' : [44.8817338462,-89.8519753846],
        'West Virginia' : [38.7460515789,-80.31806],
        'Wyoming' : [42.59952,-106.85384]
        }
    for s in statesCoordinates:
        if state == s:
            return statesCoordinates[s]
    return ""




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
            coordinates = getCoordinates2(tweet['place'])
            tweets.append(dict(zip(keys,[text,0,coordinates])))
    return tweets

def getCoordinates2(place):
    coordinatesBox =  place['bounding_box']['coordinates'][0]
    longlist = [row[0] for row in coordinatesBox]
    long = sum(longlist)/len(longlist)
    latlist = [row[1] for row in coordinatesBox]
    lat = sum(latlist)/len(latlist)
    return [lat,long]

def getText(tweet):
    if "text" in tweet:
        return tweet['text']
    else:
        return ""

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
    if minDist < 5:
        return closestState
    else:
        return ""

def calculateDistance(coord1, coord2):
    return ( (coord1[0]-coord2[0]) ** 2 + (coord1[1] - coord2[1]) ** 2) ** (0.5)

def printHappiestState(statesDict):
    state = max(statesDict.keys(), key=lambda x: statesDict[x]['score'])
    score = statesDict[state]['score']
    print state

def main():
    # Reading and parsing sentiment information
    termScores = constructDictionary()
    tweets = parseTweetFile()
    tweets = calculateTweetScores(tweets, termScores)

    statesDict = constructStatesDictionary()
    statesDict = calculateStateScores(statesDict, tweets)

    printHappiestState(statesDict)
if __name__ == '__main__':
    main()
