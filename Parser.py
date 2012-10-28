from lxml import etree

import Question
from Question import *


class Parser:
  @staticmethod
  def getRoot():
    path = "/Users/bjoveski/Dropbox/nlp dataset/Stack Exchange Data Dump - Sept 2011/Content/092011 Super User/posts.xml"
    tree = etree.parse(path)
    return tree.getroot()

  @staticmethod
  def getTags(elem):
      raw = elem.attrib.get("Tags")
      if raw != None:
        raw = raw[1:-1] 
        return set(raw.split("><")) 
      else:
        return set()
 
  @staticmethod
  def getBodyHistogram(elem):
    return None

  @staticmethod
  def getAllQuestionsFromRoot(root):
    questions = []
    for elem in root:
      if elem.attrib["PostTypeId"] == "1": ## question
        q = Question.Question(elem)
        questions.append(q)

    print("question count = %d" % len(questions))
    return questions
  
  @staticmethod
  def getQuestionsFromRoot(root, nodeCount):  
    questions = []
    for i in range(nodeCount):
      if root[i].attrib["PostTypeId"] == "1":
        q = Question.Question(root[i])
        questions.append(q)

    print("question count = %d" % len(questions))
    return questions
