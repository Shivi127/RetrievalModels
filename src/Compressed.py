import json
class CompressedIndex():
	# Methods Required for decoding the compressed Index
	K = 128

	def EncodeNum(self, n):
		K = 128
		nn = n
		b = bytearray()
		while True:
			b.append(n % self.K)
			if n < self.K: break
			n //= self.K
		b.reverse()
		b.append(self.K)
		return b

	def EncodeList(self,nums):
		b= bytearray()
		for n in nums:
			b.extend(self.EncodeNum(n))
		return b

	def DecodeByteArray(self,bytearr):
		nums = []
		n = 0
		for i in range(len(bytearr)):
			if bytearr[i] < self.K:
				n = n * self.K + bytearr[i]
			else:
				nums.append(n)
				n = 0
		return nums


	def readCLookUpIntoMemory(self):
		f = open("/Users/shivangisingh/Desktop/InformationRetrieval/CLookup.json",'r')
		LookUpTable = json.loads(f.read())
		f.close()
		return LookUpTable

# Read from disk at a current offset
	def readCompressed(self, byteoffset, bsize, breader):
		breader.seek(byteoffset)
		return self.DecodeByteArray(breader.read(bsize))


	def undelta(self,arr):
		temp = arr
		result = []
		prev_doc  = 0

		while(len(temp)>0):

			numberofterms = temp[1]
			positions = self.decode(temp[2:numberofterms+2])
			result.append(prev_doc+temp[0])
			result.append(numberofterms)
			result.extend(positions)
			prev_doc += temp[0]
			temp = temp[numberofterms+2:]

		return result

	def decode(self,decodeme):
		prev = 0
		for i, v in enumerate(decodeme):
			current = v
			decodeme[i] += prev
			prev = current
		return decodeme