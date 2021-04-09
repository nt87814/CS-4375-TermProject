# -*- coding: utf-8 -*-
"""
Created on Fri Apr  9 15:42:00 2021

@author: ntrayers
"""

from sklearn.naive_bayes import GaussianNB
import os

directory = "./train/neg"
x = []
for file in os.listdir(directory):
    with open("./train/neg/" + file, 'r', encoding="Latin-1") as f:
        x.append(f.read())
        

        
        