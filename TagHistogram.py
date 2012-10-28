import operator

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

