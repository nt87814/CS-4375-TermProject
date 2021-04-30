#Hansen Li
#Neg/Pos Only


import os.path
import math

#print("Current directory: {0}".format(os.getcwd()))
cwd = os.getcwd()

negdict: dict = dict()
posdict: dict = dict()
vocab = set()

negcount: int = 0
poscount: int = 0

negprobdict = dict()
posprobdict = dict()

filecounttrainneg = 0
filecounttrainpos = 0
probnegfilechance = 0
probposfilechance = 0

def build_dict(filename, dictionary: dict):
    text = open(filename, errors="ignore", encoding="UTF8")
    wordcount = 0
    for line in text:
        for token in line.split():
            wordcount += 1
            if token in dictionary:
                dictionary[token] += 1
            else:
                dictionary[token] = 1
    text.close()
    return wordcount

def build_vocab(vocab:set, neg: dict, pos: dict):
    for word in pos:
        vocab.add(word)
    for word in neg:
        vocab.add(word)

# Laplace smoothing, a = 1
def build_prob(dictionary: dict, probdict: dict, vocab: set, count: int):
    for word in vocab:
        if word in dictionary:
            probdict[word] = math.log(dictionary[word] + 1) - math.log(count + len(dictionary) + 1)
        else:
            probdict[word] = math.log(1) - math.log(count + len(dictionary) + 1)

def check_prob(filename, vocab: set, probdict: dict, baseprob):
    prob = math.log(baseprob)
    text = open(filename, errors="ignore", encoding="UTF8")
    for line in text:
        for token in line.split():
            if token in vocab:
                prob += probdict[token]
    text.close()
    return prob

if __name__ == "__main__":
    for filename in os.listdir(cwd+"\\files\\train\\neg"):
        negcount += build_dict(cwd+"\\files\\train\\neg\\" + filename, negdict)

    for filename in os.listdir(cwd+"\\files\\train\\pos"):
        poscount += build_dict(cwd+"\\files\\train\\pos\\" + filename, posdict)

    build_vocab(vocab, negdict, posdict)

    print("Vocab = ", len(vocab))
    print("Negcount = ", str(negcount))
    print("Poscount = ", str(poscount))

    build_prob(negdict, negprobdict, vocab, negcount)
    build_prob(posdict, posprobdict, vocab, poscount)

    trainnegfiles = next(os.walk(cwd + "\\files\\train\\neg"))[2]
    filecounttrainneg = len(trainnegfiles)

    trainposfiles = next(os.walk(cwd + "\\files\\train\\pos"))[2]
    filecounttrainpos = len(trainposfiles)

    totaltrainfiles = filecounttrainneg + filecounttrainpos

    testnegfiles = next(os.walk(cwd + "\\files\\test\\neg"))[2]
    filecounttestneg = len(testnegfiles)

    testposfiles = next(os.walk(cwd + "\\files\\test\\pos"))[2]
    filecounttestpos = len(testposfiles)

    probnegfilechance = filecounttrainneg / totaltrainfiles
    probposfilechance = filecounttrainpos / totaltrainfiles

    print("Neg file type chance: ", probnegfilechance)
    print("Pos file type chance: ", probposfilechance)

    testnegcount = 0
    testposcount = 0

    for filename in os.listdir(cwd+"\\files\\test\\neg"):
        tempneg = check_prob(cwd+"\\files\\test\\neg\\"+filename, vocab, negprobdict, probnegfilechance)
        temppos = check_prob(cwd+"\\files\\test\\neg\\"+filename, vocab, posprobdict, probposfilechance)

        if tempneg > temppos:
            testnegcount += 1

    print("Spam accuracy: ", (testnegcount / filecounttestneg))

    # Ham now
    for filename in os.listdir(cwd + "\\files\\test\\pos"):
        tempneg = check_prob(cwd+"\\files\\test\\pos\\"+filename, vocab, negprobdict, probnegfilechance)
        temppos = check_prob(cwd+"\\files\\test\\pos\\"+filename, vocab, posprobdict, probposfilechance)

        if tempneg < temppos:
            testposcount += 1

    print("Ham accuracy: ", (testposcount / filecounttestpos))

