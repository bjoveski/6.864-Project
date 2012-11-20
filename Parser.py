from lxml import etree
import lxml.html


import Question
from Question import *

import PostHistoryItem
from PostHistoryItem import *

class Parser:

  @staticmethod
  def getPostHistoryItems(start=0, end=100):
      num = end - start
      items = [None] * (num)
      (postPath, postHistoryPath) = Parser.getConfigPaths()
      tree = Parser.getPostHistoryRoot()
      for i in range(num):
        items[i] = PostHistoryItem(tree[start + i])
      return items

  @staticmethod
  def getConfigPaths():
    file_ = open("config.txt")
    postPath = file_.readline()
    postHistoryPath = file_.readline()
    file_.close()
    return (postPath[:-1], postHistoryPath)

  @staticmethod
  def getPostHistoryRoot():
    (postPath, postHistoryPath) = Parser.getConfigPaths()
    tree = etree.parse(postHistoryPath)
    return tree.getroot()

  @staticmethod
  def getAllPostHistoryItemsFromRoot(root):
    items = []
    for elem in root:
      p = PostHistoryItem(elem)
      items.append(p)
    return items

  @staticmethod
  def getRoot():
    (postPath, postHistoryPath) = Parser.getConfigPaths()
    tree = etree.parse(postPath)
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
  def getStringFromHtmlString(htmlString):
    return lxml.html.fromstring(htmlString).text_content()

 
  @staticmethod
  def getBodyHistogram(elem):
    return None

  @staticmethod
  def getAllQuestionsFromRoot(root):
    questions = []
    for elem in root:
      if elem.attrib["PostTypeId"] == "1": ## question
        q = Question(elem)
        questions.append(q)

    print("question count = %d" % len(questions))
    return questions
  
  @staticmethod
  def getQuestionsFromRoot(root, nodeCount):  
    questions = []
    for i in range(nodeCount):
      if root[i].attrib["PostTypeId"] == "1":
        q = Question(root[i])
        questions.append(q)

    print("question count = %d" % len(questions))
    return questions

  @staticmethod
  def getWordArray(string):
    return string.lower().split()
