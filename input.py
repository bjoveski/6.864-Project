#std imports
from lxml import etree
import operator
from numpy import *
import re


##local imports
# import TagHistogram
from TagHistogram import *

# import Question
from Question import *

# import Parser
from Parser import *

# from Answer import *

from PostHistoryItem import *



def getQuestions():
	return Parser.getAllQuestionsFromRoot(Parser.getRoot())

	
def getHistoryPosts():
  return Parser.getAllPostHistoryItemsFromRoot(Parser.getPostHistoryRoot())

def main():
  questions = Parser.getAllQuestionsFromRoot(Parser.getRoot())
  tagHistogram = TagHistogram()

  for question in questions:
    tagHistogram.populateHistogram(question)


  top1000pairs = tagHistogram.sortHistogram()[:1000]
  print top1000pairs
  top1000tags = [i[0] for i in top1000pairs]
  print top1000tags


def getDuplicatePostCloseTexts():
  duplicateId2Post = Parser.getDuplicatePostsIds()
  postHistory = getHistoryPosts()
  print "posts acquired"
  i = 0
  for post in postHistory:
    if post.postId in duplicateId2Post:
      duplicateId2Post[post.postId].append(post)
      i += 1
      if (i % 300 == 0):
        print "processing item %d" % i

  return duplicateId2Post


def filterTextInDuplicates():
  emptyItemsCount = 0
  duplicateId2Post = getDuplicatePostCloseTexts()
  for key in duplicateId2Post.iterkeys():
    filteredPosts = []
    for post in duplicateId2Post[key]:
      if post.postHistoryTypeId == 5:
        filteredPosts.append(post)
    duplicateId2Post[key] = filteredPosts
    if len(filteredPosts) == 0:
      emptyItemsCount += 1
  print "emptyItemsCount = %d" % emptyItemsCount
  return duplicateId2Post

def extractRegexInDuplicates(duplicateId2Post):
  histogram = {}
  for i in range(500):
    histogram[i] = 0

  out = {}  
  for key in duplicateId2Post.iterkeys():
  ##  if len((duplicateId2Post[key])) > 0:
    histogram[len(duplicateId2Post[key])] += 1
    if (len(duplicateId2Post[key])== 11):
      print key
      for i in duplicateId2Post[key]:
        print i.id, i.postId
    for copy in duplicateId2Post[key]:
      match = re.findall(r'(http://superuser.com/questions/\d*/)', copy.text)
      if (key not in out):
        out[key] = [match]
      else:
        out[key].append(match)

  for i in range(500):
    if (histogram[i] != 0):
      print i, histogram[i]
  return out

def printRegexes(duplicateId2Post):
  filePath = "/Users/bjoveski/Dropbox/nlp dataset/092011 Super User/duplicates/pairs2.txt"
  file_ = open(filePath, "w")

  for i in duplicateId2Post.iterkeys():
    for copy in duplicateId2Post[i]:
      if len(copy) > 0:
        res = copy[0].split("/")[-2] 
        file_.write("%s %s\n" % (i, int(res)))

  file_.close()
