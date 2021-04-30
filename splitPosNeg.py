# Hansen Li
# Estimate score within Pos/Neg Classification
# Pos: 7-10
# Neg: 1-4

import os.path
import math
import re

# directory
cwd = os.getcwd()
# word occurrences
wordCountPos: dict = dict()
wordCountNeg: dict = dict()
# total word score
wordScorePos: dict = dict()
wordScoreNeg: dict = dict()
# avg word scores
wordAvgScorePos: dict = dict()
wordAvgScoreNeg: dict = dict()

# total count of correct guesses
correctCountPos = 0
correctCountNeg = 0

#
trainScoreDictPos = dict()
trainScoreDictNeg = dict()
testScoreDictPos = dict()
testScoreDictNeg = dict()
guessScoreDictPos = dict()
guessScoreDictNeg = dict()

vocabPos = set()
vocabNeg = set()
totalPosTestFiles = 0
totalNegTestFiles = 0

totalcountNeg = 0
totalcountPos = 0


def build_dict(filename, wordcount: dict, wordscore: dict):
    text = open(filename, errors="ignore", encoding="UTF8")
    count = 0
    s = filename
    # gets score from filename
    # splits filename into array, first field is file number, second is score
    s = re.findall('\d+', s)
    score = int(s[1])

    for line in text:
        # print(line)
        for token in line.split():
            # print(token)
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


def score_wordNeg(worddict: dict, scoredict: dict):
    for word in worddict:
        if int(math.ceil(scoredict[word] / worddict[word])) >= 10:
            wordAvgScoreNeg[word] = 10
        else:
            wordAvgScoreNeg[word] = int(math.ceil(scoredict[word] / worddict[word]))


def score_wordPos(worddict: dict, scoredict: dict):
    for word in worddict:
        if int(math.ceil(scoredict[word] / worddict[word])) >= 10:
            wordAvgScorePos[word] = 10
        else:
            wordAvgScorePos[word] = int(math.ceil(scoredict[word] / worddict[word]))


def check_probPos(filename, vocab: set, avgscoredict: dict):
    text = open(filename, errors="ignore", encoding="UTF8")
    guessscoretotal = 0
    filewordcount = 0
    global correctCountPos
    for line in text:
        for token in line.split():
            if token in vocab:
                filewordcount += 1
                guessscoretotal += avgscoredict[token]
    text.close()
    guessScore = guessscoretotal / filewordcount

    # guessScore is float so convert to int
    # print(filewordcount)
    # print(guessscoretotal)
    guessScore = int(round(guessScore))
    # print("Actual: ", re.findall('\d+', filename)[1])
    # print("Guess: ", guessScore)
    if guessScore == int(re.findall('\d+', filename)[1]):
        #print("+1")
        correctCountPos += 1

def check_probNeg(filename, vocab: set, avgscoredict: dict):
    text = open(filename, errors="ignore", encoding="UTF8")
    guessscoretotal = 0
    filewordcount = 0
    global correctCountNeg
    for line in text:
        for token in line.split():
            if token in vocab:
                filewordcount += 1
                guessscoretotal += avgscoredict[token]
    text.close()
    guessScore = guessscoretotal / filewordcount

    # guessScore is float so convert to int
    # print(filewordcount)
    # print(guessscoretotal)
    guessScore = int(round(guessScore))
    # print("Actual: ", re.findall('\d+', filename)[1])
    # print("Guess: ", guessScore)
    if guessScore == int(re.findall('\d+', filename)[1]):
        #print("+1")
        correctCountNeg += 1

if __name__ == "__main__":
    # build word dictionary in all training files
    for filename in os.listdir(cwd + "\\files\\train\\neg"):
        totalcountNeg += build_dict(cwd + "\\files\\train\\neg\\" + filename, wordCountNeg, wordScoreNeg)
        if int(re.findall('\d+', filename)[1]) not in trainScoreDictNeg:
            trainScoreDictNeg[int(re.findall('\d+', filename)[1])] = 1
        else:
            trainScoreDictNeg[int(re.findall('\d+', filename)[1])] += 1

    for filename in os.listdir(cwd + "\\files\\train\\pos"):
        totalcountPos += build_dict(cwd + "\\files\\train\\pos\\" + filename, wordCountPos, wordScorePos)

        if int(re.findall('\d+', filename)[1]) not in trainScoreDictPos:
            trainScoreDictPos[int(re.findall('\d+', filename)[1])] = 1
        else:
            trainScoreDictPos[int(re.findall('\d+', filename)[1])] += 1

    # print(wordCount)

    # call func, find avg word score
    score_wordPos(wordCountPos, wordScorePos)
    score_wordNeg(wordCountNeg, wordScoreNeg)
    # print(wordCount["movie"])
    # print(wordScore["movie"])
    # print(wordAvgScore["movie"])
    # print(wordAvgScore)
    build_vocab(vocabPos, wordCountPos)
    build_vocab(vocabNeg, wordCountNeg)
    # print(vocab)

    for filename in os.listdir(cwd + "\\files\\test\\neg"):
        check_probNeg(cwd + "\\files\\test\\neg\\" + filename, vocabNeg, wordAvgScoreNeg)
        if int(re.findall('\d+', filename)[1]) in testScoreDictNeg:
            testScoreDictNeg[int(re.findall('\d+', filename)[1])] += 1
        else:
            testScoreDictNeg[int(re.findall('\d+', filename)[1])] = 1

    for filename in os.listdir(cwd + "\\files\\test\\pos"):
        check_probPos(cwd + "\\files\\test\\pos\\" + filename, vocabPos, wordAvgScorePos)
        if int(re.findall('\d+', filename)[1]) in testScoreDictPos:
            testScoreDictPos[int(re.findall('\d+', filename)[1])] += 1
        else:
            testScoreDictPos[int(re.findall('\d+', filename)[1])] = 1

    totalNegTestFiles += len(next(os.walk(cwd + "\\files\\test\\neg"))[2])
    totalPosTestFiles += len(next(os.walk(cwd + "\\files\\test\\pos"))[2])

    print("CCP: ", correctCountPos)
    print("CCN: ", correctCountNeg)

    accuracyPos = correctCountPos / totalPosTestFiles
    accuracyNeg = correctCountNeg / totalNegTestFiles

    print("Pos Acc: ", accuracyPos)
    print("Neg Acc: ", accuracyNeg)

    print(trainScoreDictPos)
    print(testScoreDictPos)
    print(trainScoreDictNeg)
    print(testScoreDictNeg)

    print(wordAvgScorePos)
    print("-----")
    print(wordAvgScoreNeg)
