# Hansen Li
# Notes: Results in mostly averages of 6 due to distribution of word values.
# Will modify so that it does scoring in two batches: Pos (7-10) and Neg (1-4)

import string
import os.path
import math
import re

# print("Current directory: {0}".format(os.getcwd()))
cwd = os.getcwd()


# word occurrences
wordCount: dict = dict()
# total word score
wordScore: dict = dict()
# avg word scores
wordAvgScore: dict = dict()

correctCount = 0

trainScoreDict = dict()
testScoreDict = dict()
guessScoreDict = dict()

vocab = set()
totalTestFiles = 0

totalcount = 0
#values = list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 ")

def build_dict(filename, wordcount: dict, wordscore: dict):
    text = open(filename, errors="ignore", encoding="UTF8")
    count = 0
    s = filename
    # gets score from filename
    # splits filename into array, first field is file number, second is score
    s = re.findall('\d+', s)
    score = int(s[1])

    for line in text:
        #print(line)
        for token in line.split():
            #print(token)
            count += 1
            if token in wordcount:
                # increments occurrence count and sums total score
                wordcount[token] += 1
                wordscore[token] += score
            else:
                # creates new entry with occurrence and total score
                wordcount[token] = 1
                wordscore[token] = score
    text.close()
    return count

def build_vocab(vocab: set, worddict: dict):
    for word in worddict:
        vocab.add(word)

def score_word(worddict: dict, scoredict: dict):
    for word in worddict:
        if int(math.ceil(scoredict[word] / worddict[word])) >= 10:
            wordAvgScore[word] = 10
        else:
            wordAvgScore[word] = int(math.ceil(scoredict[word] / worddict[word]))

def check_prob(filename, vocab: set, avgscoredict: dict, accuracyCount):
    text = open(filename, errors="ignore", encoding="UTF8")
    guessscoretotal = 0
    filewordcount = 0
    for line in text:
        for token in line.split():
            if token in vocab:
                filewordcount += 1
                guessscoretotal += avgscoredict[token]
    text.close()
    guessScore = guessscoretotal / filewordcount

    # guessScore is float so convert to int
    #print(filewordcount)
    #print(guessscoretotal)
    guessScore = int(round(guessScore))
    #print("Actual: ", re.findall('\d+', filename)[1])
    #print("Guess: ", guessScore)
    if guessScore == int(re.findall('\d+', filename)[1]):
        accuracyCount += 1


if __name__ == "__main__":
    # build word dictionary in all training files
    for filename in os.listdir(cwd + "\\files\\train\\neg"):
        totalcount += build_dict(cwd + "\\files\\train\\neg\\" + filename, wordCount, wordScore)
        if int(re.findall('\d+', filename)[1]) not in trainScoreDict:
            trainScoreDict[int(re.findall('\d+', filename)[1])] = 1
        else:
            trainScoreDict[int(re.findall('\d+', filename)[1])] += 1

    for filename in os.listdir(cwd + "\\files\\train\\pos"):
        totalcount += build_dict(cwd + "\\files\\train\\pos\\" + filename, wordCount, wordScore)

        if int(re.findall('\d+', filename)[1]) not in trainScoreDict:
            trainScoreDict[int(re.findall('\d+', filename)[1])] = 1
        else:
            trainScoreDict[int(re.findall('\d+', filename)[1])] += 1

    #print(wordCount)

    # call func, find avg word score
    score_word(wordCount, wordScore)
    #print(wordCount["movie"])
    #print(wordScore["movie"])
    #print(wordAvgScore["movie"])
    #print(wordAvgScore)

    build_vocab(vocab, wordCount)
    #print(vocab)

    for filename in os.listdir(cwd + "\\files\\test\\neg"):
        check_prob(cwd + "\\files\\test\\neg\\" + filename, vocab, wordAvgScore, correctCount)
        if int(re.findall('\d+', filename)[1]) in testScoreDict:
            testScoreDict[int(re.findall('\d+', filename)[1])] += 1
        else:
            testScoreDict[int(re.findall('\d+', filename)[1])] = 1

    for filename in os.listdir(cwd + "\\files\\test\\pos"):
        check_prob(cwd + "\\files\\test\\pos\\" + filename, vocab, wordAvgScore, correctCount)
        if int(re.findall('\d+', filename)[1]) in testScoreDict:
            testScoreDict[int(re.findall('\d+', filename)[1])] += 1
        else:
            testScoreDict[int(re.findall('\d+', filename)[1])] = 1

    totalTestFiles += len(next(os.walk(cwd + "\\files\\test\\neg"))[2])
    totalTestFiles += len(next(os.walk(cwd + "\\files\\test\\pos"))[2])

    accuracy = correctCount / totalTestFiles

    #print(accuracy)
    #print(trainScoreDict)
    #print(testScoreDict)

    print(wordAvgScore["no"])
