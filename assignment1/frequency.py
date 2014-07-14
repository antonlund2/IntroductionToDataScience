import sys
import json

def parseTweetFile():
    tweetFile = open(sys.argv[1])
    tweets = {} 
    for line in tweetFile:
        tweet = json.loads(line)
        if "place" in tweet and tweet["place"] is not None:
            print tweet["place"]
            
        if "text" in tweet:
            tweets.append(tweet["text"].encode('UTF8'))
        else:
            tweets.append("")
    return tweets

def createTermDictionary(tweets):
    keys= ['termFrequency','normalizedTermFrequency']
    termDictionary={}
    totalWords = 0
    for tweet in tweets:
        for word in tweet.split():
            if word != "" and word != " ":
                totalWords +=1
                if word not in termDictionary:
                    termDictionary[word]= dict(zip(keys,[1,0]))
                else:
                    termDictionary[word]['termFrequency'] += 1
    termDictionary = calculateNormalizedTermFrequency(termDictionary, totalWords)
    return termDictionary

def calculateNormalizedTermFrequency(termDictionary, totalWords):
    for term, value in termDictionary.iteritems():
        termDictionary[term]['normalizedTermFrequency']=float(value['termFrequency'])/float(totalWords)
    return termDictionary

def printTermsAndNormalizedFrequencies(termDictionary):
    for term, value in termDictionary.iteritems():
        print term, value['normalizedTermFrequency']  


def main():
    # Reading and parsing sentiment information
    tweets = parseTweetFile()
    
    #Create dictionary with all words that do not exist in semtiment filej
    termDictionary = createTermDictionary(tweets)

    printTermsAndNormalizedFrequencies(termDictionary)
if __name__ == '__main__':
    main()
