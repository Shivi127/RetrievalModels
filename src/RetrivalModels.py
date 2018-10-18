from math import log
from parse import Parse
p= Parse()
class RetrivalModel():
	# k1 	= 1.2
	# k2 	= 100
	# b 	= 0.75
	# R 	= 0.0
	# r 	= 0.0
	# N   = p.getCollectionSize()

	def BM25(self,n,f,qf,dl,avdl):
		k1 = 1.2
		k2 = 100
		b = 0.75
		R = 0.0
		r = 0.0
		N = p.getCollectionSize()

		K = self.computeK(dl, avdl,k1,b)
		first = log( ( (r + 0.5) / (R - r + 0.5) ) / ( (n - r + 0.5) / (N - n - R + r + 0.5)) )
		second = ((k1 + 1) * f) / (K + f)
		third = ((k2+1) * qf) / (k2 + qf)
		return first * second * third


	def computeK(self, dl, avdl,k1,b):
		return k1 * ((1-b) + b * (float(dl)//float(avdl)))


	def qDirichletSmoothing(self,f, mu, c, C, D):
		numerator = log(float(f) + float(mu) * (float(c)//float(C)))
		denominator = float(D) + float(mu)
		return (float(numerator)/float(denominator))



	def qlJMSmoothing(self,lam, f,c,D,C):
		return ((1-float(lam))*(float(f)/float(D)) + (float(lam))*(float(c)/float(C)))

	def vectorspace(self,f,N,ni):
		# print ("bi",f,N,ni)
		val = (1+log(float(f))) * log(1+(float(N)/float(ni)))
		print(val)
		return val