import json
# scene_textDic = {}


class Parse():
	scene_textDic = {}
	docdic = {}
	totallength = 0

	def createScenceTextDic(self):

		with open("/Users/shivangisingh/Desktop/shakespeare-scenes.json",'r') as f:
			data = json.loads(f.read())
		f.close()
		doc_count = 1

		for obj in data['corpus']:
				for k,v in obj.items():
					if k== 'sceneId':
						curr_scene = v
						if v not in self.docdic:
							self.docdic[doc_count]= v.strip()
							doc_count+=1
					if k == 'text':
						tokens = v.split(" ")
						tokenlength = len(tokens)
						self.totallength += tokenlength
						self.scene_textDic[doc_count-1] = {  "text": v,
															"lengthOfScene": tokenlength}


	def getCollectionSize(self):
		return len(self.docdic)

	def getSceneTextDic(self):
		return self.scene_textDic

	def getAvgLength(self):
		return self.totallength/self.getCollectionSize()

	def getScene(self, docID):
		return self.docdic[docID]
