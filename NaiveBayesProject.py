# -*- coding: utf-8 -*-
"""
Created on Sun May  9 01:09:40 2021

@author: james
"""

import os
import math

# Read in the files
def read():
    dict1 = {}      # Store every word that appears in a file rated 1
    dict2 = {}      # Store every word that appears in a file rated 2
    dict3 = {}      # Store every word that appears in a file rated 3
    dict4 = {}      # Store every word that appears in a file rated 4
    dict7 = {}      # Store every word that appears in a file rated 7
    dict8 = {}      # Store every word that appears in a file rated 8
    dict9 = {}      # Store every word that appears in a file rated 9
    dict10 = {}     # Store every word that appears in a file rated 10
    vocab = {}      # Store every unique word that appears in all the files
    count1 = 0      # Store number of files rated 1
    count2 = 0      # Store number of files rated 2
    count3 = 0      # Store number of files rated 3
    count4 = 0      # Store number of files rated 4
    count7 = 0      # Store number of files rated 7
    count8 = 0      # Store number of files rated 8
    count9 = 0      # Store number of files rated 9
    count10 = 0     # Store number of files rated 10
    totalCount = 0  # Store total number of files
    
    # Loop through every file in the pos directory
    for filename in os.listdir('./archive/train/train/pos'): 
        with open(os.path.join('./archive/train/train/pos', filename), 'r', encoding="Latin-1") as file:
            # If the file is rated 7
            if filename[len(filename) - 5] == '7':
                # Loop through every line and word
                for line in file:
                    for word in line.split():
                        if word in dict7:
                            dict7[word] += 1
                        else:
                            dict7[word] = 1
                        if word not in vocab:
                            vocab[word] = 1
                count7 += 1
            # If the file is rated 8
            if filename[len(filename) - 5] == '8':
                # Loop through every line and word
                for line in file:
                    for word in line.split():
                        if word in dict8:
                            dict8[word] += 1
                        else:
                            dict8[word] = 1
                        if word not in vocab:
                            vocab[word] = 1
                count8 += 1
            # If the file is rated 9
            if filename[len(filename) - 5] == '9':
                # Loop through every line and word
                for line in file:
                    for word in line.split():
                        if word in dict9:
                            dict9[word] += 1
                        else:
                            dict9[word] = 1
                        if word not in vocab:
                            vocab[word] = 1
                count9 += 1
            # If the file is rated 10
            if filename[len(filename) - 5] == '0':
                # Loop through every line and word
                for line in file:
                    for word in line.split():
                        if word in dict10:
                            dict10[word] += 1
                        else:
                            dict10[word] = 1
                        if word not in vocab:
                            vocab[word] = 1
                count10 += 1
    
    # print(dict7)
    # print(dict8)
    # print(dict9)
    # print(dict10)
        
    # Loop through every file in the neg directory        
    for filename in os.listdir('./archive/train/train/neg'): 
        with open(os.path.join('./archive/train/train/neg', filename), 'r', encoding="Latin-1") as file:
            # If the file is rated 1
            if filename[len(filename) - 5] == '1':
                # Loop through every line and word
                for line in file:
                    for word in line.split():
                        if word in dict1:
                            dict1[word] += 1
                        else:
                            dict1[word] = 1
                        if word not in vocab:
                            vocab[word] = 1
                count1 += 1
            # If the file is rated 2
            if filename[len(filename) - 5] == '2':
                # Loop through every line and word
                for line in file:
                    for word in line.split():
                        if word in dict2:
                            dict2[word] += 1
                        else:
                            dict2[word] = 1
                        if word not in vocab:
                            vocab[word] = 1
                count2 += 1
            # If the file is rated 3
            if filename[len(filename) - 5] == '3':
                # Loop through every line and word
                for line in file:
                    for word in line.split():
                        if word in dict3:
                            dict3[word] += 1
                        else:
                            dict3[word] = 1
                        if word not in vocab:
                            vocab[word] = 1
                count3 += 1
            # If the file is rated 4
            if filename[len(filename) - 5] == '4':
                # Loop through every line and word
                for line in file:
                    for word in line.split():
                        if word in dict4:
                            dict4[word] += 1
                        else:
                            dict4[word] = 1
                        if word not in vocab:
                            vocab[word] = 1
                count4 += 1
   
    # Calculate the total number of files
    totalCount = count1 + count2 + count3 + count4 + count7 + count8 + count9 + count10
    
    # Calculate the percentage each rated file makes up of the total
    per1 = count1 / totalCount
    per2 = count2 / totalCount
    per3 = count3 / totalCount
    per4 = count4 / totalCount
    per7 = count7 / totalCount
    per8 = count8 / totalCount
    per9 = count9 / totalCount
    per10 = count10 / totalCount
    
    return dict1, dict2, dict3, dict4, dict7, dict8, dict9, dict10, per1, per2, per3, per4, per7, per8, per9, per10, vocab
    
# Calculate the probablity of each word appearing in a specific rated file
def prob(dict1, dict2, dict3, dict4, dict7, dict8, dict9, dict10, vocab):
    
    total1 = dictSum(dict1)     # Store total number of words in files rated 1
    total2 = dictSum(dict2)     # Store total number of words in files rated 2
    total3 = dictSum(dict3)     # Store total number of words in files rated 3
    total4 = dictSum(dict4)     # Store total number of words in files rated 4
    total7 = dictSum(dict7)     # Store total number of words in files rated 7
    total8 = dictSum(dict8)     # Store total number of words in files rated 8
    total9 = dictSum(dict9)     # Store total number of words in files rated 9
    total10 = dictSum(dict10)   # Store total number of words in files rated 10
    vocabTotal = len(vocab)     # Store total number of unique words 
    
    probs1 = {}     # Store probablilty of each word being in a file rated 1
    probs2 = {}     # Store probablilty of each word being in a file rated 2
    probs3 = {}     # Store probablilty of each word being in a file rated 3
    probs4 = {}     # Store probablilty of each word being in a file rated 4
    probs7 = {}     # Store probablilty of each word being in a file rated 7
    probs8 = {}     # Store probablilty of each word being in a file rated 8
    probs9 = {}     # Store probablilty of each word being in a file rated 9
    probs10 = {}    # Store probablilty of each word being in a file rated 10
    
    # Calculate the probability of each word being in a specifically rated file
    for i in dict1:
        probs1[i] = (dict1[i] + 1) / (total1 + vocabTotal)
    for i in dict2:
        probs2[i] = (dict2[i] + 1) / (total2 + vocabTotal)
    for i in dict3:
        probs3[i] = (dict3[i] + 1) / (total3 + vocabTotal)
    for i in dict4:
        probs4[i] = (dict4[i] + 1) / (total4 + vocabTotal)
    for i in dict7:
        probs7[i] = (dict7[i] + 1) / (total7 + vocabTotal)
    for i in dict8:
        probs8[i] = (dict8[i] + 1) / (total8 + vocabTotal)
    for i in dict9:
        probs9[i] = (dict9[i] + 1) / (total9 + vocabTotal)
    for i in dict10:
        probs10[i] = (dict10[i] + 1) / (total10 + vocabTotal)
        
    return probs1, probs2, probs3, probs4, probs7, probs8, probs9, probs10
        
# Classify a file as a rating 1-4 or 7-10 and return the accuracy
def classify(probs1, probs2, probs3, probs4, probs7, probs8, probs9, probs10, per1, per2, per3, per4, per7, per8, per9, per10):
    
    corr1 = 0       # Store the number of files correctly classified as a file rated 1
    corr2 = 0       # Store the number of files correctly classified as a file rated 2
    corr3 = 0       # Store the number of files correctly classified as a file rated 3
    corr4 = 0       # Store the number of files correctly classified as a file rated 4
    corr7 = 0       # Store the number of files correctly classified as a file rated 7
    corr8 = 0       # Store the number of files correctly classified as a file rated 8
    corr9 = 0       # Store the number of files correctly classified as a file rated 9
    corr10 = 0      # Store the number of files correctly classified as a file rated 10
    count1 = 0      # Store total number of files rated 1
    count2 = 0      # Store total number of files rated 2
    count3 = 0      # Store total number of files rated 3
    count4 = 0      # Store total number of files rated 4
    count7 = 0      # Store total number of files rated 7
    count8 = 0      # Store total number of files rated 8
    count9 = 0      # Store total number of files rated 9
    count10 = 0     # Store total number of files rated 10
    
    # Loop through each file in the neg directory and classify them as a rating 1-4
    for filename in os.listdir('./archive/test/test/neg'): 
        prob1 = 0
        prob2 = 0
        prob3 = 0
        prob4 = 0
        with open(os.path.join('./archive/test/test/neg', filename), 'r', encoding="Latin-1") as file:
            for line in file:
                for word in line.split():
                    if word in probs1:
                        prob1 += math.log(probs1[word], 10)
                    if word in probs2:
                        prob2 += math.log(probs2[word], 10)
                    if word in probs3:
                        prob3 += math.log(probs3[word], 10)
                    if word in probs4:
                        prob4 += math.log(probs4[word], 10)
        prob1 += math.log(per1, 10)
        prob2 += math.log(per2, 10)
        prob3 += math.log(per3, 10)
        prob4 += math.log(per4, 10)
        
        # Classify the files and determine if the classification is correct
        if filename[len(filename) - 5] == '1':
            count1 += 1
            if max(prob1, prob2, prob3, prob4) == prob1:
                corr1 += 1
        if filename[len(filename) - 5] == '2':
            count2 += 1
            if max(prob1, prob2, prob3, prob4) == prob2:
                corr2 += 1
        if filename[len(filename) - 5] == '3':
            count3 += 1
            if max(prob1, prob2, prob3, prob4) == prob3:
                corr3 += 1
        if filename[len(filename) - 5] == '4':
            count4 += 1
            if max(prob1, prob2, prob3, prob4) == prob4:
                corr4 += 1
    
    # Loop through each file in the pos directory and classify them as a rating 7-9
    for filename in os.listdir('./archive/test/test/pos'):
        prob7 = 0
        prob8 = 0
        prob9 = 0
        prob10 = 0
        with open(os.path.join('./archive/test/test/pos', filename), 'r', encoding="Latin-1") as file:
            for line in file:
                for word in line.split():
                    if word in probs7:
                        prob7 += math.log(probs7[word], 10)
                    if word in probs8:
                        prob8 += math.log(probs8[word], 10)
                    if word in probs9:
                        prob9 += math.log(probs9[word], 10)
                    if word in probs10:
                        prob10 += math.log(probs10[word], 10)
        prob7 += math.log(per7, 10)
        prob8 += math.log(per8, 10)
        prob9 += math.log(per9, 10)
        prob10 += math.log(per10, 10)
        
        # Classify the files and determine if the classification is correct
        if filename[len(filename) - 5] == '7':
            count7 += 1
            if max(prob7, prob8, prob9, prob10) == prob7:
                corr7 += 1
        if filename[len(filename) - 5] == '8':
            count8 += 1
            if max(prob7, prob8, prob9, prob10) == prob8:
                corr8 += 1
        if filename[len(filename) - 5] == '9':
            count9 += 1
            if max(prob7, prob8, prob9, prob10) == prob9:
                corr9 += 1
        if filename[len(filename) - 5] == '0':
            count10 += 1
            if max(prob7, prob8, prob9, prob10) == prob10:
                corr10 += 1
                
    return corr1, corr2, corr3, corr4, corr7, corr8, corr9, corr10, count1, count2, count3, count4, count7, count8, count9, count10
                
# Return the sum of a dictionary (total # of words in files)
def dictSum(dicts):
    
    totalSum = 0
    for i in dicts:
        totalSum += dicts[i]
    return totalSum

if __name__ == '__main__':
    # Run algorithm
    dict1, dict2, dict3, dict4, dict7, dict8, dict9, dict10, per1, per2, per3, per4, per7, per8, per9, per10, vocab = read()
    probs1, probs2, probs3, probs4, probs7, probs8, probs9, probs10 = prob(dict1, dict2, dict3, dict4, dict7, dict8, dict9, dict10, vocab)
    corr1, corr2, corr3, corr4, corr7, corr8, corr9, corr10, count1, count2, count3, count4, count7, count8, count9, count10 = classify(probs1, probs2, probs3, probs4, probs7, probs8, probs9, probs10, per1, per2, per3, per4, per7, per8, per9, per10)
    
    # Calculate accuracy as percentages
    perCorr1 = corr1 / count1 * 100
    perCorr2 = corr2 / count2 * 100
    perCorr3 = corr3 / count3 * 100
    perCorr4 = corr4 / count4 * 100
    perCorr7 = corr7 / count7 * 100
    perCorr8 = corr8 / count8 * 100
    perCorr9 = corr9 / count9 * 100
    perCorr10 = corr10 / count10 * 100
    avgCorr = (perCorr1 + perCorr2 + perCorr3 + perCorr4 + perCorr7 + perCorr8 + perCorr9 + perCorr10) / 8
        
    print()
    print("Percetage of 1-Rated Reviews Correctly Classified:  {:.2f}%".format(perCorr1))
    print("Percetage of 2-Rated Reviews Correctly Classified:  {:.2f}%".format(perCorr2))
    print("Percetage of 3-Rated Reviews Correctly Classified:  {:.2f}%".format(perCorr3))
    print("Percetage of 4-Rated Reviews Correctly Classified:  {:.2f}%".format(perCorr4))
    print("Percetage of 7-Rated Reviews Correctly Classified:  {:.2f}%".format(perCorr7))
    print("Percetage of 8-Rated Reviews Correctly Classified:  {:.2f}%".format(perCorr8))
    print("Percetage of 9-Rated Reviews Correctly Classified:  {:.2f}%".format(perCorr9))
    print("Percetage of 10-Rated Reviews Correctly Classified:  {:.2f}%".format(perCorr10))
    print("Average Accuracy: {:.2f}%".format(avgCorr))