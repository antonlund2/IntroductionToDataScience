import sys
import json

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
    keys = ['text' ,'score']
    scoredTweets = []
    for tweet in tweets:
        score = 0
        words = tweet.split(" ") 
        for word in words:
            if word in scores:
                score += scores[word]
        scoredTweets.append(dict(zip(keys,[tweet,score])))
    return scoredTweets

def printTweetScores(scoredTweets):
    for tweet in scoredTweets:
        print tweet['score']

def createTermDictionary(scores,scoredTweets):
    keys = ['termScore','termFrequency','normalizedTermScore']
    termDictionary={}
    
    for tweet in scoredTweets:
        for word in tweet['text'].split(" "):
            if word not in scores:
                if word not in termDictionary:
                    termDictionary[word]= dict(zip(keys,[tweet['score'],1,0]))
                else:
                    termDictionary[word]['termScore'] += tweet['score']
                    termDictionary[word]['termFrequency'] += 1
    return termDictionary

def printTermsAndScores(termDictionary):
    for term, value in termDictionary.iteritems():
        print term + " " + str(value['termScore'])

def main():
    # Reading and parsing sentiment information
    scores = constructDictionary()

    tweets = parseTweetFile()
    
    scoredTweets = calculateTweetScores(tweets, scores)
    
    #For printing all tweet scores
    #printTweetScores(scoredTweets)    

    #Create dictionary with all words that do not exist in semtiment filej
    termDictionary = createTermDictionary(scores,scoredTweets)

    printTermsAndScores(termDictionary)
if __name__ == '__main__':
    main()
