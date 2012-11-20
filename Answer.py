from lxml import etree
import operator
from numpy import *

#local imports
import Parser
from Parser import *

class Answer:

  def __init__(self, elem):
    self.body = elem.attrib["Body"]
    self.title = elem.attrib["Title"]
    self.score = int(elem.attrib["Score"])
    self.tags = Parser.Parser.getTags(elem)
    self.bodyString = Parser.Parser.getStringFromHtmlString(self.body)


  def populateTitleVector(self, titleHistogram):
    self.titleVector = zeros(titleHistogram.vocabSize, dtype = int16)
    for word in Parser.Parser.getWordArray(self.title):
      if (word in titleHistogram.word2index):
        index = titleHistogram.word2index[word]
        self.titleVector[index] = 1

  def compareTitles(self, question):
    vec1 = self.titleVector 
    vec2 = question.titleVector
    norm1 = inner(vec1, vec1)
    norm2 = inner(vec2, vec2)
    if (norm1 != 0 and norm2 != 0):
      return inner(vec1, vec2) / (math.sqrt(norm1) * math.sqrt(norm2))
    else:
      return 0
