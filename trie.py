class symbol(object):
	def __init__(self, type, value, span):
	  	self.type = type
	    self.value = value
	    self.span = span
	    
	def __repr__(self):
	    return "{ \"t\":" + str([self.type, self.value]) + ", \"s\":" + str(self.span[0]) + ", \"e\":" + str(self.span[1]) + "}"
		
class Trie: #should I add (object) parameter as above? - ROB > TALI
	def __init__(self, trie={}):
		self.trie = trie
		self.extras = []
		self.branches = {} #extra branches for diff
		
	def add(self, word, token, diff=False):
		level = self.trie
		length = len(word)
		for i in range(length - 1): #all characters except the last
			char = word[i]
			
			if not level[char]:
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
		if not level[char]:
			level[char] = {}
		if not level[char]["to"]:
			level[char]["to"] = []
		level[char]["to"].append(token)
	
	def diff(self):
		for prefix in self.extras:
			node = self.trie
			for char in prefix:
				node = node[char]
			self.branches[prefix] = node[prefix[-1]]
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
					while !level[char] and re.match("\s", char):
						char = string[end]
						end += 1
						
				node = level[char]
				if node and node == 1:
					node = fetch_record(string[begin:end]) #what should I use for file IO here? ROB > TALI
					level[char] = node #reconnects the branch
					
				if node:
					for token in node["to"]:
						tokens.append(symbol(token[0], token[1], [begin, end]))
					level = node
				else: break
			begin += 1
			end = begin
			level = self.trie
		return tokens
			