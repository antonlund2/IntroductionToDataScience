import sys
import json

def lines(fp):
    print str(len(fp.readlines()))


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
    for line in tweetFile:
        tweet = json.loads(line)
        if "text" in tweet:
            tweets.append(tweet["text"].encode('UTF8'))
        else:
            tweets.append("")
    return tweets

def calculateTweetScores(tweets, scores):
    tweetScores = []
    for tweet in tweets:
        score = 0
        words = tweet.split(" ") 
        for word in words:
            if word in scores:
                score += scores[word]
        tweetScores.append(score)
    return tweetScores

def printTweetScores(tweetScores):
    for score in tweetScores:
        print score



def main():
    # Reading and parsing sentiment information
    scores = constructDictionary()

    tweets = parseTweetFile()
    
    tweetScores = calculateTweetScores(tweets, scores)

    printTweetScores(tweetScores)    

if __name__ == '__main__':
    main()
