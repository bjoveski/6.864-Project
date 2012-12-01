from lxml import etree
import lxml.html
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from time import time

import Question
from Question import *

import PostHistoryItem
from PostHistoryItem import *

class Parser:


  """
  returns (dictionary, bigram)
  dictionary[word] = 
  """
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



  '''
  returns dict whose keys are the words, and values are [index, count]
  '''
  @staticmethod
  def Sort_Dictionary(D):
    new_Dict={}
    c = 0
    StopWords=stopwords.words('english')
    notRemove = ["which", "who", "when", "where", "why", "how", "what", "don", "should", "not"]
    for i in notRemove:
      StopWords.remove(i)
    D_sorted = sorted(D.iteritems(), key = operator.itemgetter(1), reverse=True)
    for i in D_sorted:
      # if key not in stopwords
      if i[0] not in StopWords:
        # if value greater than 1
        if i[1] > 1:
          new_Dict[i[0]]=[c]
          new_Dict[i[0]].append(i[1])
          c+=1
    return new_Dict


## bojan note: same function as sort_dictionary
  ''' 
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
  '''



  @staticmethod
  def evaluate_vector(sentence,dictionary_general,dictionary_tags,bigram):
    general_vector=[[],[],[]]
    word_vector=[[],[],[]]
    bigram_vector=[[],[],[]]
    c = 0
    print "begin"
    tokenizer=RegexpTokenizer("[\w']+")
    S=tokenizer.tokenize(sentence.lower())
    for i in S:
      print "i=%s" % i
      if i in dictionary_general:
        print "i in dictionary_general"
        if i in general_vector[0]:
          general_vector[2][general_vector[0].index(i)]+=1
        else:
          general_vector[0].append(i)
          general_vector[1].append(dictionary_general[i])
          general_vector[2].append(1)
      if i in dictionary_tags:
        print "i in dictionary_tags"
        if i in word_vector[0]:
          word_vector[2][word_vector[0].index(i)]+=1
        else:
          word_vector[0].append(i)
          word_vector[1].append(dictionary_tags[i][0])
          word_vector[2].append(1)
        j=1
        bigram_test=i
        print "####"
        print dictionary_tags[i][1]
        print "#####"
        while j< len(dictionary_tags[i][1]):
          print "c=%d, j=%d, dictionary_tags[i][1]=%d i=%s" % (c, j, len(dictionary_tags[i][1]),  i)
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
  def generateGlobalDictionaryUnfiltered(path):
    tokenizer = RegexpTokenizer("[\w']+")
    globalDict = {}
    lineId = 0
    last = 0

    file_ = open(path)
    for line in file_:
      lineId += 1
      if (lineId % 5000 == 0):
        print "processing lineId=%5d, dict_size=%5d, delta=%5d" % (lineId, len(globalDict), len(globalDict) - last)
        last = len(globalDict)
      S = tokenizer.tokenize(line)
      for token in S:
        if token in globalDict:
          globalDict[token] += 1
        else:
          globalDict[token] = 1
    file_.close()
    print "done generateGlobalDictionaryUnfiltered"
    return globalDict


  @staticmethod
  def outputAllVectorsToFile(filePath, globalDict, tagsDict, bigramDict):
    file_ = open(filePath, "w")
    globalDict_ = sorted(globalDict.iteritems(), key=operator.itemgetter(1), reverse=True)
    Parser.printVector(file_, globalDict_)
    
    tagsDict_ = sorted(tagsDict.iteritems(), key=operator.itemgetter(1), reverse=True)
    Parser.printVector(file_, tagsDict_)

    bigramDict_ = sorted(bigramDict.iteritems(), key=operator.itemgetter(1), reverse=True)
    Parser.printVector(file_, bigramDict_)
    file_.close()

  @staticmethod
  def printVector(file_, sorted_):
    #file_.write("%d\n" % len(sorted_))
    for (key, value) in sorted_:
      file_.write("%s,%s," % (key, value))
    file_.write("\n")

  @staticmethod
  def outputDictionaryToFile(dictionary, filePath):    
    file_ = open(filePath, "w")
    sorted_ = sorted(dictionary.iteritems(), key=operator.itemgetter(1), reverse=True)
    ##sorted_ = sorted(dictionary.iteritems(), key=lambda (k,v): operator.itemgetter(1)(v), reverse=True)
    
    for (key, value) in sorted_:
      file_.write("%s,%s" % (key, value))
    file_.close()

  @staticmethod
  def generateGlobalTagsFile():
    questions = Parser.getAllQuestionsFromRoot(Parser.getRoot())
    (tags, bigrams) = Parser.Generate_Tags_Dictionary(questions)
    sortedTags = Parser.Sort_Dictionary(tags)
    sortedBigrams = Parser.sort_dictionary(bigrams)

    outputDictionaryToFile(sorted_tags, sorted_pat)



  @staticmethod
  def generateGlobalDictFile():
    rawQuestionsPath = "/Users/bjoveski/classes/6.864/diego_data/preproc"
    outputFilteredDictPath = "/Users/bjoveski/classes/6.864/diego_data/filteredDict"

    unfilteredDict = Parser.generateGlobalDictionaryUnfiltered(rawQuestionsPath)
    filteredDict = Parser.Sort_Dictionary(unfilteredDict) ## fileterd[word] = [index, count]

    print("done processing global dict")
    
    Parser.outputDictionaryToFile(filteredDict, outputFilteredDictPath)

    return (unfilteredDict, filteredDict)


  @staticmethod
  def createDictionaryFromFilePath(path):
    file_ = open(path)
    dict = {}
    for line in file_:
      (item, index) = line.split(",")
      dict[item] = int(index)
    return dict

  @staticmethod
  def generateVector(string, word2IndexDict):
    tokenizer = RegexpTokenizer("[\w']+")
    tokens = tokenizer.tokenize(string.lower())
    resultVector = {}
    for token in tokens:
      if (token in word2IndexDict):
        index = word2IndexDict[token]
        if index in resultVector:
          resultVector[index] += 1
        else:
          resultVector[index] = 1
    return resultVector

  @staticmethod
  def generateBigramVector(string, bigramDict, bigramDictTokens):
    tokenizer = RegexpTokenizer("[\w']+")
    words = tokenizer.tokenize(string.lower())
    resultVector = {}
    for bigram in bigramDict.iterkeys():
      tokens = bigramDictTokens[bigram]
      if (tokens[0]) not in words:
        continue;

      for start_word_index in xrange(len(words) - len(tokens) + 1):
        # start from each word
        success = True
        for token_index in xrange(len(tokens)):          
          if (words[start_word_index + token_index] != tokens[token_index]):
            success = False
            break;
        if success == True:
          if bigramDict[bigram] in resultVector:
           resultVector[bigramDict[bigram]] += 1
          else:
            resultVector[bigramDict[bigram]] = 1
          continue;
    return resultVector    

  
  """
  @staticmethod
  def generateVectorFile(inputFilePath, outputFilePath, globalDict, tagsDict, bigramDict):
    titleLineId = 1
    ContentLineId = 2
    TagLineId = 3
    AnswerLineId = 4
    string = Parser.readKthLineInFile(inputFilePath, ContentLineId)
    
    Parser.outputAllVectorsToFile(outputFilePath, 
      Parser.generateVector(string, globalDict),
      Parser.generateVector(string, tagsDict),
      Parser.generateVector(string, bigramDict))
  """  

  @staticmethod
  def generateBIGRAM_EVERYTHING():
    globalDictPath = "/Users/bjoveski/Dropbox/nlp dataset/092011 Super User/dictionaries/word2Index"
    tagDictPath = "/Users/bjoveski/Dropbox/nlp dataset/092011 Super User/dictionaries/tag2Index"
    bigramDictPath = "/Users/bjoveski/Dropbox/nlp dataset/092011 Super User/dictionaries/bigram2Index"

#    globalDict = Parser.createDictionaryFromFilePath(globalDictPath)
#    tagsDict = Parser.createDictionaryFromFilePath(tagDictPath)
    bigramDict = Parser.createDictionaryFromFilePath(bigramDictPath)
   
    bigramDictTokens = {}
    for bigram in bigramDict:
      bigramDictTokens[bigram] = bigram.split("-")

    titleLineId = 1
    ContentLineId = 2
    TagLineId = 3
    AnswerLineId = 4

    idPath = "/Users/bjoveski/Dropbox/nlp dataset/092011 Super User/id.txt"
    idfile = open(idPath)
    questionIds = []
    for line in idfile:
      questionIds.append(int(line))
    
    startTime = time()
    currTime = time()

    outputFolder = "/Users/bjoveski/Dropbox/nlp dataset/092011 Super User/vectors/descriptions/"
    
    startTime = time()
    currTime = time()    
    ## global dict
    
    DICTIONARY = bigramDict
    
    FILENAME = "%s/%s" % (outputFolder, "vector_description_bigrams.txt")
    LINEID = ContentLineId
    Parser.generateAllBigramVectors(LINEID, questionIds, FILENAME, DICTIONARY, bigramDictTokens)
    print "done vector_description_global timeTaken=%f" % (time() - currTime)
    currTime = time()
    

    FILENAME = "%s/%s" % (outputFolder, "vector_title_bigrams.txt")
    LINEID = titleLineId
    Parser.generateAllBigramVectors(LINEID, questionIds, FILENAME, DICTIONARY, bigramDictTokens)
    print "done vector_description_global timeTaken=%f" % (time() - currTime)
    currTime = time()

    FILENAME = "%s/%s" % (outputFolder, "vector_answer_bigrams.txt")
    LINEID = AnswerLineId
    Parser.generateAllBigramVectors(LINEID, questionIds, FILENAME, DICTIONARY, bigramDictTokens)
    print "done vector_description_global timeTaken=%f" % (time() - currTime)
    currTime = time()

    FILENAME = "%s/%s" % (outputFolder, "vector_tag_bigrams.txt")
    LINEID = TagLineId
    Parser.generateAllBigramVectors(LINEID, questionIds, FILENAME, DICTIONARY, bigramDictTokens)
    print "done vector_description_global timeTaken=%f" % (time() - currTime)
    currTime = time()
    print "#########"



  @staticmethod
  def generateEVERYTHING():
    globalDictPath = "/Users/bjoveski/Dropbox/nlp dataset/092011 Super User/dictionaries/word2Index"
    tagDictPath = "/Users/bjoveski/Dropbox/nlp dataset/092011 Super User/dictionaries/tag2Index"
    bigramDictPath = "/Users/bjoveski/Dropbox/nlp dataset/092011 Super User/dictionaries/bigram2Index"

    globalDict = Parser.createDictionaryFromFilePath(globalDictPath)
    tagsDict = Parser.createDictionaryFromFilePath(tagDictPath)
    bigramDict = Parser.createDictionaryFromFilePath(bigramDictPath)
   
    titleLineId = 1
    ContentLineId = 2
    TagLineId = 3
    AnswerLineId = 4

    idPath = "/Users/bjoveski/Dropbox/nlp dataset/092011 Super User/id.txt"
    idfile = open(idPath)
    questionIds = []
    for line in idfile:
      questionIds.append(int(line))
    
    startTime = time()
    currTime = time()

    outputFolder = "/Users/bjoveski/Dropbox/nlp dataset/092011 Super User/vectors/descriptions/"
    
    startTime = time()
    currTime = time()    
    ## global dict
    DICTIONARY = globalDict
    
    '''
    FILENAME = "%s/%s" % (outputFolder, "vector_description_global.txt")
    LINEID = ContentLineId
    Parser.generateAllVectors(LINEID, questionIds, FILENAME, DICTIONARY)
    print "done vector_description_global timeTaken=%f" % (time() - currTime)
    currTime = time()
    '''

    FILENAME = "%s/%s" % (outputFolder, "vector_title_global.txt")
    LINEID = titleLineId
    Parser.generateAllVectors(LINEID, questionIds, FILENAME, DICTIONARY)
    print "done vector_description_global timeTaken=%f" % (time() - currTime)
    currTime = time()

    FILENAME = "%s/%s" % (outputFolder, "vector_answer_global.txt")
    LINEID = AnswerLineId
    Parser.generateAllVectors(LINEID, questionIds, FILENAME, DICTIONARY)
    print "done vector_description_global timeTaken=%f" % (time() - currTime)
    currTime = time()

    FILENAME = "%s/%s" % (outputFolder, "vector_tag_global.txt")
    LINEID = TagLineId
    Parser.generateAllVectors(LINEID, questionIds, FILENAME, DICTIONARY)
    print "done vector_description_global timeTaken=%f" % (time() - currTime)
    currTime = time()
    print "#########"


    DICTIONARY = tagsDict
    
    
    FILENAME = "%s/%s" % (outputFolder, "vector_description_tags.txt")
    LINEID = ContentLineId
    Parser.generateAllVectors(LINEID, questionIds, FILENAME, DICTIONARY)
    print "done vector_description_global timeTaken=%f" % (time() - currTime)
    currTime = time()
    

    FILENAME = "%s/%s" % (outputFolder, "vector_title_tags.txt")
    LINEID = titleLineId
    Parser.generateAllVectors(LINEID, questionIds, FILENAME, DICTIONARY)
    print "done vector_description_global timeTaken=%f" % (time() - currTime)
    currTime = time()

    FILENAME = "%s/%s" % (outputFolder, "vector_answer_tags.txt")
    LINEID = AnswerLineId
    Parser.generateAllVectors(LINEID, questionIds, FILENAME, DICTIONARY)
    print "done vector_description_global timeTaken=%f" % (time() - currTime)
    currTime = time()

    FILENAME = "%s/%s" % (outputFolder, "vector_tag_tags.txt")
    LINEID = TagLineId
    Parser.generateAllVectors(LINEID, questionIds, FILENAME, DICTIONARY)
    print "done vector_description_global timeTaken=%f" % (time() - currTime)
    currTime = time()
    print "#########"



    DICTIONARY = bigramDict
    
    FILENAME = "%s/%s" % (outputFolder, "vector_description_bigrams.txt")
    LINEID = ContentLineId
    Parser.generateAllVectors(LINEID, questionIds, FILENAME, DICTIONARY)
    print "done vector_description_global timeTaken=%f" % (time() - currTime)
    currTime = time()
    

    FILENAME = "%s/%s" % (outputFolder, "vector_title_bigrams.txt")
    LINEID = titleLineId
    Parser.generateAllVectors(LINEID, questionIds, FILENAME, DICTIONARY)
    print "done vector_description_global timeTaken=%f" % (time() - currTime)
    currTime = time()

    FILENAME = "%s/%s" % (outputFolder, "vector_answer_bigrams.txt")
    LINEID = AnswerLineId
    Parser.generateAllVectors(LINEID, questionIds, FILENAME, DICTIONARY)
    print "done vector_description_global timeTaken=%f" % (time() - currTime)
    currTime = time()

    FILENAME = "%s/%s" % (outputFolder, "vector_tag_bigrams.txt")
    LINEID = TagLineId
    Parser.generateAllVectors(LINEID, questionIds, FILENAME, DICTIONARY)
    print "done vector_description_global timeTaken=%f" % (time() - currTime)
    currTime = time()
    print "#########"


  @staticmethod
  def generateAllBigramVectors(lineId, questionIds,fileName, dict, chuckedDict):
    startTime = time()
    currTime = time()
    file_ = open(fileName, "w")

    for i in range(len(questionIds)):
      if (i % 1000 == 0):
        print "proccessing done=%2fpct, timeTaken=%f" % ( i * 100.0/len(questionIds), time() - currTime)
        currTime = time()
      inputFilePath = "/Users/bjoveski/Dropbox/nlp dataset/092011 Super User/preproc/q_full_%d.txt" % questionIds[i]      
      string = Parser.readKthLineInFile(inputFilePath, lineId)
      vectorDict = Parser.generateBigramVector(string, dict, chuckedDict)
      Parser.writeSparceVector(file_, questionIds[i], vectorDict)

    file_.close()
    print "done. totalTime=%f" % (time() - startTime)



  @staticmethod
  def generateAllVectors(lineId, questionIds,fileName, dict):
    startTime = time()
    currTime = time()
    file_ = open(fileName, "w")

    for i in range(len(questionIds)):
      if (i % 5000 == 0):
        print "proccessing done=%2fpct, timeTaken=%f" % ( i * 100.0/len(questionIds), time() - currTime)
        currTime = time()
      inputFilePath = "/Users/bjoveski/Dropbox/nlp dataset/092011 Super User/preproc/q_full_%d.txt" % questionIds[i]      
      string = Parser.readKthLineInFile(inputFilePath, lineId)
      vectorDict = Parser.generateVector(string, dict)
      Parser.writeSparceVector(file_, questionIds[i], vectorDict)

    file_.close()
    print "done. totalTime=%f" % (time() - startTime)

  @staticmethod  
  def writeSparceVector(file_, questionId, dict):
    file_.write("%d," %questionId)
    dict_ = sorted(dict.iteritems(), key=operator.itemgetter(1), reverse=True)
    Parser.printVector(file_, dict_)


  @staticmethod
  def readKthLineInFile(filePath, lineId):
    curr_line = 0
    with open(filePath) as file_:
      for line in file_:
        if curr_line != lineId:
          curr_line += 1
        else:
          return line

  



'''
outputFilteredDictPath = "/Users/bjoveski/classes/6.864/diego_data/tag2Index"
sorted_ = sorted(dictionary.iteritems(), key=lambda (k,v): operator.itemgetter(1)(k))

>>> file_ = open(outputFilteredDictPath, "w")
>>> for (key, value) in sorted_:
  file_.write("%s,%s,%s\n" % (key, value[0] + 1, value[1]))





>>> dictPath = "/Users/bjoveski/classes/6.864/diego_data/word2Index"
>>> dict = Parser.createDictionaryFromFilePath(dictPath)
>>> inputPath = "/Users/bjoveski/Dropbox/nlp dataset/092011 Super User/preproc/q_full_1.txt"
>>> outputPath = "/Users/bjoveski/Dropbox/nlp dataset/092011 Super User/vectors/titles/q_title_1.txt"
>>> a = Parser.generateVectorFile(inputPath, outputPath, dict)


'''



