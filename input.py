#std imports
from lxml import etree
import operator

##local imports
import TagHistogram
from TagHistogram import *

import Question
from Question import *

import Parser
from Parser import *




def main():
  questions = Parser.getAllQuestionsFromRoot(Parser.getRoot())
  tagHistogram = TagHistogram()

  for question in questions:
    tagHistogram.populateHistogram(question)


  top1000pairs = tagHistogram.sortHistogram()[:1000]
  print top1000pairs
  top1000tags = [i[0] for i in top1000pairs]
  print top1000tags





  



    
