from lxml import etree
import operator
from numpy import *

#local imports
import Parser
from Parser import *


class Question:

  def __init__(self, elem):
    self.body = elem.attrib["Body"]
    self.title = elem.attrib["Title"]
    self.score = int(elem.attrib["Score"])
    self.tags = Parser.Parser.getTags(elem)


  def populateTitleVector(self, titleHistogram):
  	self.titleVector = zeros(titleHistogram.vocabSize, dtype = int16)
  	for word in Parser.Parser.getWordArray(self.title):
  		if (word in titleHistogram.word2index):
  			index = titleHistogram.word2index[word]
  			self.titleVector[index] = 1

  def compareTitles(self, question):
  	vec1 = self.titleVector 
  	vec2 = question.titleVector
  	return inner(vec1, vec2) / (norm(vec1) * norm(vec2))
  	


