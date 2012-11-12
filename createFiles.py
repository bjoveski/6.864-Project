#std imports
from lxml import etree
import operator
from numpy import *
import nltk
from nltk.tag.simplify import simplify_wsj_tag
from nltk.corpus import wordnet

##local imports
# import TagHistogram
from TagHistogram import *

# import Question
from Question import *

# import Parser
from Parser import *


def get_tokens(x):
        y = nltk.word_tokenize(x.lower())
        #apply filters
        return y

def tagging(x):
        tokens = get_tokens(x)
        tagged = nltk.pos_tag(tokens)
        simple = ["/".join([word,simplify_wsj_tag(tag)]) for word,tag in tagged]
        y = " ".join(simple)
        return y


count = 0
root = Parser.getRoot()
for elem in root:
        if elem.attrib["PostTypeId"] == "1": ## question
                print("QUESTION %d" % count)
                filestr = 'data/ques_%d.txt' % count
                #file_ = open(filestr, 'w')
                body = elem.attrib["Body"]
                title = elem.attrib["Title"]
                score = int(elem.attrib["Score"])
                tags = Parser.getTags(elem)
                bodyString = lxml.html.fromstring(body).text_content()
                print "TITLE"
                print tagging(title)
                print "BODY"
                print tagging(bodyString)
                print ""
                #print>>file_, item
                #file_.close()
                count += 1
                if count == 10:
                        break
        
