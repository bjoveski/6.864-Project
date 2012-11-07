#This is a file to run my draft code

import re
import math
import itertools
import nltk
from nltk.tag.simplify import simplify_wsj_tag
from nltk.corpus import wordnet


def cossim(x,y):
    a=set(x)
    b=set(y)
    return len(a & b)/math.sqrt(len(a)*len(b))

def filter_words(tokens): #filter nouns and verbs
    t = nltk.pos_tag(tokens)
    filt = []
    for word, tag in t:
        simptag = simplify_wsj_tag(tag)
        if simptag == 'N':
            filt.append([word,'n'])
        elif simptag == 'V':
            filt.append([word,'v'])
    return filt

def wordsim(x,y):
    reducx = filter_words(x)
    reducy = filter_words(y)
    sim = 0
    count = -0.1
    for wordx,tagx in reducx:
        for (wordy,tagy) in reducy:
            a = wordnet.synsets(wordx,tagx)
            b = wordnet.synsets(wordy,tagy)
            if (len(a)>0 and len(b)>0):
                wsim = a[0].wup_similarity(b[0])
                if wsim != None:
                    sim = sim + wsim
                count = count +1
                #print(sim)
    return sim/count
    


# title, description, answer, tags for some questions

# http://superuser.com/questions/56540/
q1 = '32-bit vs. 64-bit systems'
d1 = 'What are the differences between 32-bit and 64-bit systems? If you have used both of them, what kind of sharp differences have you experienced? Would it be a problem to use 32-bit programs on 64-bit systems in some cases?'
t1 = ['64-bit','operating-systems','32-bit ','computer-architecture ','cpu-architecture']
a1 = 'Note: These answers apply to standard PC CPUs (Intel and AMD) and Windows (as typically configured for end-users). Other 32-bit or 64-bit chips, other OSes, and other OS configurations can have different tradeoffs. From a technical perspective, a 64-bit OS gives you: Allows individual processes to address more than 4 GB of RAM each (in practice, most but not all 32-bit OSes also limit the total usable system RAM to less than 4 GB, not just the per-application maximum). All pointers take 8 bytes instead of 4 bytes. The effect on RAM usage is minimal (because youre not likely to have an application filled with gigabytes of pointers), but in the worst theoretical case, this can make the CPU cache be able to hold 1/2 as many pointers (making it be effectively 1/2 the size). For most applications, this is not a huge deal. There are many more general-purpose CPU registers in 64-bit mode. Registers are the fastest memory in your entire system. There are only 8 in 32-bit mode and 16 general purpose registers in 64-bit mode. In scientific computing applications Ive written, Ive seen up to a 30% performance boost by recompiling in 64-bit mode (my application could really use the extra registers). Most 32-bit OSes really only let individual applications use 2 GB of RAM, even if you have 4 GB installed. This is because the other 2 GB of address space is reserved for sharing data between applications, with the OS, and for communicating with drivers. Windows and Linux will let you adjust this tradeoff to be 3 GB for applications and 1 GB shared, but this can cause problems for some applications that dont expect the change. Im also guessing it might cripple a graphics card that has 1 GB of RAM (but Im not sure). A 64-bit OS can give individual 32-bit applications closer to the full 4 GB to play with. From a users perspective: Application speed is usually faster for a 64-bit application in a 64-bit OS compared to the 32-bit version of the application on a 32-bit OS, but most users wont see this speed-up. Most applications for normal users dont really take advantage of the extra registers or the benefits are balanced out by bigger pointers filling up the cache. If you have any memory hog applications (like photo editors, video processing, scientific computing, etc.), if you have (or can buy) more than 3 GB of RAM, and you can get a 64-bit version of the application, the choice is easy: use the 64-bit OS. Some hardware doesnt have 64-bit drivers. Check your motherboard, all plug-in cards, and all USB devices before making the switch. Note that in the early days of Windows Vista, there were lots of problems with drivers. These days things are generally better. If you run so many applications at a time that youre running out of RAM (usually you can tell this because your computer starts getting really slow and you hear the hard disk drive crunching), then youll want a 64-bit OS (and sufficient RAM). You can run 32-bit applications (but not drivers) in 64-bit Windows with no problems. The worst slowdown Ive measured for a 32-bit application in 64-bit Windows is about 5% (meaning that if it took 60 seconds to do something in 32-bit Windows, it took at most 60/0.95 = 63 seconds with the same 32-bit application in 64-bit Windows).'

# http://superuser.com/questions/10370/
# copy of q1
q2 = 'What is the difference between 64-bit and 32-bit Operating systems?'
d2 = 'I know that there are 2 types of OSs, 64 bit and 32 bit What is the main differences between them? And if I am buying a new laptop, which one should i install? It will be able to run all applications if I installed either of them? I am talking mainly about windows Operating systems, but you can answer about others as well.'
t2 = ['64-bit','operating-systems','32-bit']
a2 = 'mainly the amount of RAM accessible. In most 32bit OSs there is a 4gb (closer to 3gb actually) ceiling. I believe vista x64 can access up to 128gb. Realistically, unless youre a power user it wont matter. Very few activities youd do on a daily basis will require more than 3gb of memory. Also, driver support for 32bit OSs is slightly better. 64bit apps will not run in a 32bit environment. However, you probably wont find very many apps that are exclusively 64bit. 32bit apps will run fine 99% of the time in x64.'

# http://superuser.com/questions/4526/
# related to q1
q3 = 'Should I install 64-bit versions of operating systems?'
d3 = 'With the release of Windows 7 coming up, 64-bit operating systems have caught my attention. What are the main advantages and disadvantages of installing 64-bit Windows 7? What type of compatibility issues will I face and would i have to install 64-bit software, or will all the applications I have been using in 32-bit operating systems work just the same? Edit: My computer is only 5 months old, so it supports 64-bit operating systems'
t3 = ['windows-7','windows','64-bit','operating-systems']
a3 = 'Yes absolutely. I havent encountered any hardware or program issues. All of your 32-bit applications should work fine. Mine have. Windows 7 has got to have the best hardware support Windows has ever had'

# http://superuser.com/questions/83137/
# related to q6
q4 = 'Do i have 32-bit or 64-bit?'
d4 = 'I have manually installed Windows 7 Ultimate on my AMD on 32-bit, but i am not sure if i have 32 or 64 bit. My Windows 7 System (CP) tells me i have a 32-bit OS, but that my processor is a AMD Athlon64. So, do i have a 32 or 64 bit? Is it better to use 64 bit? I dont think so, a lot of programs tell at their websites only 32-bit. it still works, but that would be because i have installed w7 as 32-bit.'
t4 = ['windows-7','64-bit','32-bit']
a4 = 'You have a 32bit OS on 64bit capable hardware. Basically, this means you CAN use a 64bit OS, but you dont have to. Theres really little point unless you have >3GB of RAM. Compatibility issues are mainly a thing of the past, too - 64bit architecture can emulate 32bit architecture just fine in the vast, vast majority of cases.'

# http://superuser.com/questions/115662/how-can-i-find-out-which-version-of-windows-7-i-am-running-64-bit-or-32-bit?rq=1
# copy of q6
q5 = 'How can I find out which version of Windows 7 I am running? 64-bit or 32-bit?'
d5 = 'How can I find out which version of Windows 7 I am running? 64-bit or 32-bit?'
t5 = ['windows-7','64-bit ','32-bit']
a5 = 'Right click Computer->properties. Under system look at "system type", there you have it.'

# http://superuser.com/questions/96092/os-version-32-bit-or-64-bit
q6 = 'OS version: 32-bit or 64-bit?'
d6 = 'Whats the command line to find out if the OS is running a 32-bit version or 64-bit of Windows?'
t6 = ['windows','computer-architecture','cpu-architecture','windows-edition']
a6 = 'I can not attach answer to another post so here. Piping the result of systeminfo - is taking a quite good amount in time and writes to the console so is not the best solution for command files (batch scripts - anyhow You like to call them B-) ). Even with the findstr - it does not find this on other language version of windows. On a central european language win7 os it also returns ..."X86-based"... on the result but something other on then the "type" were looking for. I am not sure that it can vary on other language variants of the os. Probably the "wmic" method is the most reliable - it asks the os directly. Other possible quick solution can be to examine a variable (at least working on win7 at me). echo %PROCESSOR_ARCHITECTURE% Ok - it is quite long to remember but possible a set + findstr ARCH can be remembered. Sure - some can modify a system variable so not that reliable than wmic. But can be used quickly. I hope I could help someone out.'

lstWords = set([])
q = [0]*6
q[0] = nltk.word_tokenize(q1.lower())
q[1] = nltk.word_tokenize(q2.lower())
q[2] = nltk.word_tokenize(q3.lower())
q[3] = nltk.word_tokenize(q4.lower())
q[4] = nltk.word_tokenize(q5.lower())
q[5] = nltk.word_tokenize(q6.lower())
d = [0]*6
d[0] = nltk.word_tokenize(d1.lower())
d[1] = nltk.word_tokenize(d2.lower())
d[2] = nltk.word_tokenize(d3.lower())
d[3] = nltk.word_tokenize(d4.lower())
d[4] = nltk.word_tokenize(d5.lower())
d[5] = nltk.word_tokenize(d6.lower())
t = [0]*6
t[0] = t1
t[1] = t2
t[2] = t3
t[3] = t4
t[4] = t5
t[5] = t6
a = [0]*6
a[0] = nltk.word_tokenize(a1.lower())
a[1] = nltk.word_tokenize(a2.lower())
a[2] = nltk.word_tokenize(a3.lower())
a[3] = nltk.word_tokenize(a4.lower())
a[4] = nltk.word_tokenize(a5.lower())
a[5] = nltk.word_tokenize(a6.lower())
qa = [0]*6
qa[0] = q[0]+d[0]+a[0]+t[0]
qa[1] = q[1]+d[1]+a[1]+t[1]
qa[2] = q[2]+d[2]+a[2]+t[2]
qa[3] = q[3]+d[3]+a[3]+t[3]
qa[4] = q[4]+d[4]+a[4]+t[4]
qa[5] = q[5]+d[5]+a[5]+t[5]

print("cosine similarity")
for j in range(6):
    print("Q%d" % j),
    for i in range(6):
        print("%.6f" %  cossim(d[i],d[j])),
    print
    
print("semantic similarity")
for j in range(6):
    print("Q%d" % j),
    for i in range(6):
        print("%.6f" %  wordsim(d[i],d[j])),
    print

