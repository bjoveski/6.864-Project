from lxml import etree
import operator

import Parser
from Parser import *


class Question:

  def __init__(self, elem):
    self.body = elem.attrib["Body"]
    self.title = elem.attrib["Title"]
    self.score = int(elem.attrib["Score"])
    self.tags = Parser.getTags(elem)