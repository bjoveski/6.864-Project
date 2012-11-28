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
    my_ascii = htmlString.encode('ascii', 'ignore')
    return lxml.html.fromstring(my_ascii).text_content()
    #return nltk.util.clean_html(my_ascii)

 
  @staticmethod
  def getBodyHistogram(elem):
    return None

  @staticmethod
  def getAllQuestionsFromRoot(root):
    path = Parser.getConfigPaths()[0][0:-9]+'preproc/'
    questions = []
    for elem in root:
      if elem.attrib["PostTypeId"] == "1": ## question
        q = Question(elem)
        #questions.append(q)
        q.populateAnswer(root)
        file_ = open(path + 'q_full_' +q.id+ '.txt'  , 'w')
        q.printQuestion(file_)

    print("question count = %d" % len(questions))
    return questions
  
  @staticmethod
  def findIdFromRoot(root, I):
    lo = 0
    hi = len(root)
    while lo < hi:
        mid = (lo+hi)//2
        midval = int(root[mid].attrib["Id"])
        if midval < I:
            lo = mid+1
        elif midval > I: 
            hi = mid
        else:
            return root[mid]
    return []
  

  @staticmethod
  def getQuestionsFromRoot(root, start,end):
    path = Parser.getConfigPaths()[0][0:-9]+'preproc/'
    questions = []
    for i in range(start,end):
      if root[i].attrib["PostTypeId"] == "1":
        q = Question(root[i])
        #questions.append(q)
        q.populateAnswer(root)
        file_ = open(path + 'q_full_' +q.id+ '.txt'  , 'w')
        q.printQuestion(file_)
      if (i%50)==0:
        print i

    print("question count = %d" % len(questions))
    return questions

  @staticmethod
  def getWordArray(string):
    return string.lower().split()

