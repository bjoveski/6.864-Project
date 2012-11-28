from lxml import etree
import operator
from numpy import *

#local imports
import Parser
from Parser import *

import Answer
from Answer import *


class Question:

  def __init__(self, elem):
    self.id = elem.attrib["Id"]
    self.body = elem.attrib["Body"]
    self.title = elem.attrib["Title"]
    self.score = int(elem.attrib["Score"])
    self.tags = Parser.Parser.getTags(elem)
    self.bodyString = Parser.Parser.getStringFromHtmlString(self.body)
    self.ans_count = 0
    if ("AnswerCount" in elem.attrib):
      self.ans_count = int(elem.attrib["AnswerCount"])
    self.ans_id = -1
    self.answer = []
    if ("AcceptedAnswerId" in elem.attrib):
      self.ans_id = int(elem.attrib["AcceptedAnswerId"])

  def printQuestion(self,file_):
    print>>file_,self.score
    print>>file_,self.title.encode('ascii', 'ignore').lower().replace('\n', ' ')
    print>>file_,self.bodyString.encode('ascii', 'ignore').lower().replace('\n', ' ')
    print>>file_," ".join(self.tags)
    ans = ''
    if(self.answer):
        ans = self.answer.bodyString.encode('ascii', 'ignore').lower().replace('\n', ' ')
    print>>file_,ans
    print>>file_,self.ans_count

  def populateAnswer(self,root):
    if (self.ans_id>=0):
      elem = Parser.Parser.findIdFromRoot(root,self.ans_id)
      if (elem):
        self.answer = Answer(elem)
      else:
        self.ans_id = -1

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


  def findMostSimilarTitle(self, questions):
    maxSimilarity = 0
    mostSimilar = None
    norm1 = math.sqrt(inner(self.titleVector, self.titleVector))
    if norm1 == 0:
      return (None, 0)
    else:
      for q in questions:
        if (q != self):
          norm2sq = inner(q.titleVector, q.titleVector)
          if (norm2sq != 0):
            similarity = inner(q.titleVector, self.titleVector) / (norm1 * math.sqrt(norm2sq))
            if (similarity > maxSimilarity):
              maxSimilarity = similarity
              mostSimilar = q
      return (mostSimilar, maxSimilarity)
