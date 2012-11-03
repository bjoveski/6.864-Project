import operator

import Parser
from Parser import *

class TagHistogram:
  def __init__(self):
    self.histogram = {}

  def populateHistogram(self, question):
    for tag in question.tags:
      if tag in self.histogram:
        self.histogram[tag] += 1;
      else:
        self.histogram[tag] = 1;

  def sortHistogram(self):
    return sorted(self.histogram.iteritems(), key = operator.itemgetter(1), reverse=True)


class TitleHistogram:
  def __init__(self):
    self.histogram = {}


  def __init__(self, histogram):
    self.histogram = histogram

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



