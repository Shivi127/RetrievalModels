# import queue
import operator
from math import log
from Compressed import CompressedIndex
from RetrivalModels import RetrivalModel
from parse import Parse


p = Parse()
p.createScenceTextDic()
scene_textDic = p.getSceneTextDic()
c = CompressedIndex()
r = RetrivalModel()

class TRetrival:
	ULookup = c.readCLookUpIntoMemory()
	idfDic 	= {}


	def __init__(self):
		self.idfDic = {}
		self.totalNumberofWords = 0
		self.N = p.getCollectionSize()


	termCInvertedListDic ={}

	def processInvertedList(self, word, arr):
		self.termCInvertedListDic[word]= {}
		ni = self.ULookup[word]['#ofdocumnetsInCollection']
		self.idf(word,ni)

		while(len(arr)>0):
			docID = arr[0]
			termFrequencyinDoc = arr[1]
			self.termCInvertedListDic[word][docID]= {"tfd" 			: termFrequencyinDoc,
													 "lengthofDoc"  : scene_textDic[docID]['lengthOfScene'],
													 "ni"			: ni}
			arr = arr[2+termFrequencyinDoc:]

	def idf(self,w,ni):
		if w not in self.idfDic:
			self.idfDic[w]= log(self.N//ni)

	def getC(self):

		for key,values in self.ULookup.items():
			self.totalNumberofWords += values["#ofoccurancesInCollection"]


	def TermAtATime(self, Q, topK , model):

		A = {}
		termCInvertedListDic = {}

		breader = open("/Users/shivangisingh/Desktop/InformationRetrieval/CIndex.txt",'rb')
		# Just in case we are Using QL, I dont have to initialize it again and again
		self.getC()

		for q in Q:
			if q not in self.ULookup:
				continue
			byteoffset = self.ULookup[q]['offset']
			bsize = self.ULookup[q]['size']
			arr = c.undelta(c.readCompressed(byteoffset, bsize, breader))
			arr = self.processInvertedList(q,arr)
		breader.close()



		for word,valueDic in self.termCInvertedListDic.items():
			for k,v in valueDic.items():
				score = self.VectorSpace(word,k)
				print ("The Score is" , score)
				if k not in A:
					A[k] = self.VectorSpace(word,k)

				else:
					A[k] = A[k] + self.VectorSpace(word,k)

		A = sorted(A.items(), key = operator.itemgetter(1), reverse=True)
		return A[:topK]


	def Scoring(self, score,word, k, Q):
		# k = docID
		if score == 'BM25':
			print("I am in 25")
			self.BM25Scoring(word, k, Q.count(word))
		elif score == 'Dirichlet':
			self.QLDirichlet(word,k)
		elif score == 'JMercier':
			self.QLJM(word,k)
		elif score == "vector-space":
			self.VectorSpace(word,k)

	def BM25Scoring(self,w,docID,qf):

		n 	= self.termCInvertedListDic[w][docID]['ni']
		f 	= self.termCInvertedListDic[w][docID]['tfd']
		qf 	= qf
		dl 	= self.termCInvertedListDic[w][docID]['lengthofDoc']
		avdl= p.getAvgLength()

		return r.BM25(n,f,qf,dl,avdl)


	def QLDirichlet(self,word,docID):
		# print("ULookUp",self.ULookup[word])
		c	= self.termCInvertedListDic[word][docID]['tfd']
		mu 	= 0.4
		f   = self.ULookup[word]['#ofoccurancesInCollection']
		C	= self.totalNumberofWords
		D	= self.termCInvertedListDic[word][docID]['lengthofDoc']
		return r.qDirichletSmoothing(f,mu,c,C,D)


	def QLJM(self,word,docID):
		lam = 0.6
		f = self.termCInvertedListDic[word][docID]['tfd']
		c	= self.ULookup[word]['#ofoccurancesInCollection']
		D	= self.termCInvertedListDic[word][docID]['lengthofDoc']
		C	= self.totalNumberofWords
		return r.qlJMSmoothing(lam,f,c,D,C)

	def VectorSpace(self,word,docID):
		f 	= self.termCInvertedListDic[word][docID]['tfd']
		return r.vectorspace(f,self.N, self.termCInvertedListDic[word][docID]['ni'])

