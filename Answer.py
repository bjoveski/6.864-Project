from lxml import etree
import operator
from numpy import *

#local imports
import Parser
from Parser import *

class Answer:

  def __init__(self, elem):
    self.body = ''
    self.bodyString = ''
    self.parentId = elem.attrib["ParentId"]
    if ("Body" in elem.attrib):
      self.body = elem.attrib["Body"]
      self.bodyString = Parser.Parser.getStringFromHtmlString(self.body)

  def populateTitleVector(self, titleHistogram):
    self.titleVector = zeros(titleHistogram.vocabSize, dtype = int16)
    for word in Parser.Parser.getWordArray(self.title):
      if (word in titleHistogram.word2index):
        index = titleHistogram.word2index[word]
        self.titleVector[index] = 1

  def printAnswer(self,file_):
    print>>file_,self.bodyString.encode('ascii', 'ignore').lower().replace('\n', ' ')
