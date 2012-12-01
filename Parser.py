from lxml import etree
import lxml.html
from nltk.tokenize import RegexpTokenizer

import Question
from Question import *

import PostHistoryItem
from PostHistoryItem import *

class Parser:

  @staticmethod
  def Generate_Tags_Dictionary(Q):
    bigram={}
    dictionary={}
    for i in Q:
      for j in i.tags:
        w=j.split("-")
        for t in w:
          if t.lower() in dictionary:
            dictionary[t.lower()][0] +=1
          else:
            dictionary[t.lower()]=[1,1]
            
        if '-' in j:
          if dictionary[w[0]][1]<len(w):
            dictionary[w[0]][1]=len(w)
          if j.lower() in bigram:
            bigram[j.lower()] +=1
          else:
            bigram[j.lower()]=1

    return dictionary,bigram



  @staticmethod
  def Sort_Dictionary(D):
    new_Dict={}
    c=0
    StopWords=stopwords.words('english')
    notRemove = ["which", "who", "when", "where", "why", "how", "what", "don", "should", "not"]
    for i in notRemove:
      StopWords.remove(i)
    D_sorted=sorted(D.iteritems(), key = operator.itemgetter(1), reverse=True)
    for i in D_sorted:
      if i[0] not in StopWords:
        if i[1] >1:
          new_Dict[i[0]]=[c]
          new_Dict[i[0]].append(i[1])
          c+=1
    return new_Dict

  @staticmethod
  def Sort_Tags_Dictionary(D):
    new_Dict={}
    c=0
    StopWords=stopwords.words('english')
    notRemove = ["which", "who", "when", "where", "why", "how", "what", "don", "should", "not"]
    for i in notRemove:
      StopWords.remove(i)
    D_sorted=sorted(D.iteritems(), key = operator.itemgetter(1), reverse=True)
    for i in D_sorted:
      if i[0] not in StopWords:
        if i[1][0] >1:
          new_Dict[i[0]]=[c]
          new_Dict[i[0]].extend(i[1])
          c+=1
    return new_Dict
  

  @staticmethod
  def evaluate_vector(sentence,dictionary_general,dictionary_tags,bigram):
    general_vector=[[],[],[]]
    word_vector=[[],[],[]]
    bigram_vector=[[],[],[]]
    c=0
    tokenizer=RegexpTokenizer("[\w']+")
    S=tokenizer.tokenize(sentence.lower())
    for i in S:
      if i in dictionary_general:
        if i in general_vector[0]:
          general_vector[2][general_vector[0].index(i)]+=1
        else:
          general_vector[0].append(i)
          general_vector[1].append(dictionary_general[i])
          general_vector[2].append(1)
      if i in dictionary_tags:
        if i in word_vector[0]:
          word_vector[2][word_vector[0].index(i)]+=1
        else:
          word_vector[0].append(i)
          word_vector[1].append(dictionary_tags[i][0])
          word_vector[2].append(1)
        j=1
        bigram_test=i
        while j<dictionary_tags[i][1]:
          bigram_test+='-'
          if((c+j) <len(S)):
            bigram_test+=S[c+j]
          if bigram_test in bigram:
            if bigram_test in bigram_vector[0]:
              bigram_vector[2][bigram_vector[0].index(bigram_test)]+=1
            else:
              bigram_vector[0].append(bigram_test)
              bigram_vector[1].append(bigram[bigram_test])
              bigram_vector[2].append(1)
          j+=1
      c+=1
    return general_vector,word_vector,bigram_vector




  @staticmethod
  def getPostHistoryItems(start=0, end=100):
      num = end - start
      items = [None] * (num)      
      tree = Parser.getPostHistoryRoot()
      print "gotten tree"
      for i in range(num):
        if (i % 100 == 0):
          print "acquiring item %d, id= %d " % (i,  start + i)
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


  @staticmethod
  def getDuplicatePostsIds():
    path = "/Users/bjoveski/Dropbox/nlp dataset/092011 Super User/duplicates/duplicate_posts_id.txt"
    file_ = open(path)
    
    duplicatePostsDict = {}
 
    for line in file_:      
      duplicatePostsDict[int(line)] = []
    file_.close()

    return duplicatePostsDict


  @staticmethod
  def generateGlobalDictionaryUnfiltered():
    folderPath = "/Users/bjoveski/Dropbox/nlp dataset/092011 Super User/preproc"
    number_indeces = 2
    tokenizer = RegexpTokenizer("[\w']+")
    globalDict = {}

    for i in range(1, number_indeces):
      path = "%s/q_full_%s.txt" % (folderPath, i)
      file_ = open(path)
      for line in file_:
        S = tokenizer.tokenize(line)
        for token in S:
          if token in globalDict:
            globalDict[token] += 1
          else:
            globalDict[token] = 1
      file_.close()

    return globalDict

  @staticmethod
  def outputDictionaryToFile(dictionary):
    filePath = "/Users/bjoveski/Dropbox/nlp dataset/092011 Super User/globalDictUnfiltered.txt"
    file_ = open(filePath, "w")
    for key in dictionary.iterkeys():
      file_.write("%s %s\n" % (key, dictionary[key]))

    file_.close()


  @staticmethod
  def createDictionaryFromFilePath(path):
    file_ = open(path)
    dict = {}
    for line in file_:
      (item, count) = line.split(" ")
      dict[item] = int(count)
    return dict
