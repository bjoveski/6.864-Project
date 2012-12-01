from nltk.tokenize import RegexpTokenizer


import operator

import Parser
from Parser import *



class TagHistogram:
  def __init__(self):
    self.histogram = {}
    self.bigrams = {}

  def populateHistogram(self, question):
    for tag in question.tags:
      tokens = tag.split("-")
      for token in tokens:
        if token in self.histogram:
          self.histogram[token] += 1;
        else:
          self.histogram[token] = 1;
      if len(tokens) > 1:
        if tag in self.bigrams:
          self.bigrams[tag] += 1;
        else:
          self.bigrams[tag] = 1;

  def sortHistogram(self):
    return sorted(self.histogram.iteritems(), key = operator.itemgetter(1), reverse=True)

  def createHistogram(self, questions, threshold):
    for q in questions:
      self.populateHistogram(q)

class TitleHistogram:
  def __init__(self):
    self.histogram = {}


  #def __init__(self, histogram):
  #  self.histogram = histogram

  def populateHistogram(self, question):
    for word in Parser.getWordArray(question.title):
      if word in self.histogram:
        self.histogram[word] += 1
      else:
        self.histogram[word] = 1

  def sortHistogram(self):
    return sorted(self.histogram.iteritems(), key = operator.itemgetter(1), reverse=True)

 

  def pruneHistogram(self, threshold):
    newHist = dict((key, val) for key, val in self.histogram.iteritems() if val > threshold)
    self.histogram = newHist


  def initWord2Index(self):
    self.word2index = {}
    index = 0
    for key in self.histogram.iterkeys():
      self.word2index[key] = index
      index += 1

    self.vocabSize = len(self.word2index)


  def createHistogram(self, questions, threshold):
    for q in questions:
      self.populateHistogram(q)
    self.pruneHistogram(threshold)
    self.initWord2Index()


"""
 sorted(th.bigrams.iteritems(), key = operator.itemgetter(1), reverse=True)

>>> path = "/Users/bjoveski/classes/6.864/diego_data/tag2indexWCount"
>>> file_ = open(path, "w")
>>> index = 1

 for i in tokensSorted:
  print "%s,%d,%d\n" % (i[0], index, i[1])
  index += 1




"""


