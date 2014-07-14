import sys
import json



def parseTweetFile():
    tweetFile = open(sys.argv[1])
    tagDictionary = {}
    for line in tweetFile:
        tweet = json.loads(line)
        if "entities" in tweet:
            hashtags = tweet['entities']['hashtags']
            if hashtags != "":
                for tag in hashtags:
                    hashtag = tag['text'].encode('UTF8')
                    if hashtag in tagDictionary:
                        tagDictionary[hashtag] +=1
                    else:
                        tagDictionary[hashtag] = 1
    return tagDictionary

def printTweetScores(tagDictionary):
    top10 = sorted(tagDictionary, key=tagDictionary.get, reverse=True)[:10]
    for tag in top10:
        print tag, tagDictionary[tag]

def main():
    tagDictionary = parseTweetFile()
    printTweetScores(tagDictionary)

if __name__ == '__main__':
    main()
