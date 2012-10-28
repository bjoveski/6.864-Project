from lxml import etree
import operator

def main():
  questions = Parser.getAllQuestionsFromRoot(Parser.getRoot())
  tagHistogram = TagHistogram()

  for question in questions:
    tagHistogram.populateHistogram(question)


  top1000pairs = tagHistogram.sortHistogram()[:1000]
  print top1000pairs
  top1000tags = [i[0] for i in top1000pairs]
  print top1000tags



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





class Question:

  def __init__(self, elem):
    self.body = elem.attrib["Body"]
    self.title = elem.attrib["Title"]
    self.score = int(elem.attrib["Score"])
    self.tags = Parser.getTags(elem)

  



    