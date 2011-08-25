import os, json, re

def fetch_record(prefix): #loading a branch from a file
	name = os.path.abspath("branches/" + prefix + ".txt")
	if os.path.isfile(name):
		f = open(name, "r")
		return json.loads(f.read())
	else:
		return {}
	f.close()
		
def create_record(prefix, data):
	if not os.path.isdir("branches"):
		os.makedirs("branches")
	name = os.path.abspath("branches/" + prefix + ".txt")
	f = open(name, "w")
	dat = json.dumps(data)
	f.write(dat)
	f.close()

class symbol(object):
	def __init__(self, type, value, span):
	  	self.type = type
		self.value = value
		self.span = span
	def __repr__(self):
	    return "{ \"t\":" + str([self.type, self.value]) + ", \"s\":" + str(self.span[0]) + ", \"e\":" + str(self.span[1]) + "}"
		
class trie:
	def __init__(self, trie={}):
		self.trie = trie
		self.extras = []
		#self.branches = {} #extra branches for diff
		
	def add(self, word, token, diff=False):
		level = self.trie
		length = len(word)
		for i in range(length - 1): #all characters except the last
			char = word[i]
			if not level.get(char, False):
				if diff:
					newQ = True
					for prefix in self.extras:
						if word[:len(prefix)] == prefix:
							newQ = False
							break
					if newQ:
						self.extras.append(word[:i+1])
				level[char] = {}
			level = level[char]
									# the last character
		char = word[length-1]
		if not level.get(char, False):
			level[char] = {}
		if not level[char].get("to", False):
			level[char]["to"] = []
		level[char]["to"].append(token)
		
	def diff(self):
		for prefix in self.extras:
			node = self.trie
			for char in prefix[0:-1]:
				node = node[char]
			create_record(prefix, node[prefix[-1]]) #self.branches[prefix] = node[prefix[-1]]
			node[prefix[-1]] = 1 #1 is a special value that tells the tokenizer that this branch must be fetched
		
	def tokenize(self, string, ignore_whitespace=False):
		tokens = []
		level = self.trie
		begin = end = 0
		length = len(string)
		while begin < length:
			while level and level != {} and end < length:
				char = string[end]
				end += 1
				if ignore_whitespace:#skip over all the whitespace characters that don't help
					while (not level[char]) and re.match("\s", char):
						char = string[end]
						end += 1
				node = level.get(char, False)
				if node and node == 1:
					node = fetch_record(string[begin:end]) 
					level[char] = node #reconnects the branch
					
				if node:
					for token in node.get("to",[]):
						#lookahead for whitespace
						while end<len(string) and re.match("\s",string[end]):
							end = end+1
						tokens.append(symbol(token[0], token[1], [begin, end]))
					level = node
				else: break
			begin += 1
			end = begin #pretty deep
			level = self.trie

		def post_tokenize(st,tok):
			holes = [0 for i in st]
			h_spans = []
			for t in tok:
				for c in range(t.span[0],t.span[1]):
					holes[c] = 1
			for h in range(len(holes)):
				if holes[h]==0 and (h==0 or holes[h-1]==1):
					h_spans.append(h)
				elif holes[h]==1 and h!=0 and holes[h-1]==0:
					h_spans.append(h)
			
			returns = [symbol("hole",st[h_spans[i]:h_spans[i+1]],[h_spans[i],h_spans[i+1]]) for i in range(0,len(h_spans),2) if re.search("[A-Za-z]",st[h_spans[i]:h_spans[i+1]])]
			tok.extend(returns)
			return tok
				
		tokens = post_tokenize(string, tokens)
		print tokens
		return tokens
		
	def save(self):
		create_record("__init__",self.trie)
		
	def load(self):
		self.trie = fetch_record("__init__")