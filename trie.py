## trie.py now requires ZODB 3.3.1 be installed ##

import os, re, transaction
from ZODB.FileStorage import FileStorage
from ZODB.DB import DB
from persistent.mapping import PersistentMapping

class db:
	def __init__(self, file="trie.fs"):
		self.file = file
		self.open()
	def open(self):
		self.method = FileStorage(self.file)
		self.store = DB(self.method)
		self.connection = self.store.open()
		self.root = self.connection.root()
	def close(self):
		transaction.commit()
		self.store.close()
	def get(self, prefix, alt=None):
		return self.root.get(prefix,alt)
	def set(self, prefix, data):
		self.root[prefix] = data
		return data
	def clear(self):
		for entry in self.root.keys():
			del self.root[entry]
		transaction.commit()
	def commit(self):
		transaction.commit()

class symbol(object):
	def __init__(self, type, value, span, pop=0):
	  	self.type = type
		self.value = value
		self.span = span
		self.pop = pop
	def __repr__(self):
	    return "{ \"t\":" + str([self.type, self.value]) + ", \"s\":" + str(self.span[0]) + ", \"e\":" + str(self.span[1]) + ", \"pop\":" + str(self.pop) + "}"
	    
class trie_dict(PersistentMapping):
	def __init__(self, max_tokens=250):
		PersistentMapping.__init__(self)
		self.count = 0
		self.max_tokens = max_tokens

#########################TRIE#########################

class trie:
	def __init__(self, keystore="trie", max_tokens=250):
		self.keystore = keystore
		self.max_tokens = max_tokens
		self.load()
		#self.extras = []
		#self.branches = {} #extra branches for diff
		
	def load(self):
		self.db = db(self.keystore+".fs")
		self.trie = self.db.get("__init__",False)
		if not self.trie:
			self.trie = self.db.set("__init__",trie_dict(self.max_tokens))
			
	def save(self):
		self.trie._p_changed = 1
		self.db.commit()
		
	def clear(self):
		self.db.clear()
		self.trie = self.db.set("__init__",trie_dict(max))
		
	def finish(self): #only use if you're sure you're done
		self.db.close()
		
	def add(self, word, token, ):
		token.append(0)
		level = self.trie
		length = len(word)
		self.trie.count += 1
		diff = self.trie.count > self.max_tokens
			
		for i in range(length): #all characters except the last
			char = word[i]
			next_level = level.get(char, False)
			prefix = word[:i+1]
			if not next_level:
				if diff:
					next_level = self.db.set(prefix, trie_dict(self.trie.max_tokens))
					level[char] = 1
					next_level.count+=1
					diff = next_level.count > next_level.max_tokens
				else:
					next_level = {}
					level[char] = next_level
			elif next_level==1:
				next_level = self.db.get(prefix,{}) #I no longer reattach the unsnapped branch
				diff = next_level.count > next_level.max_tokens
			level = next_level
			
			if i==length-1:	#the last character
				if not level.get("to", False):
					level["to"] = []
				#print token
				level["to"].append(token)
		
	def tokenize(self, string, ignore="[^A-Za-z0-9]"):
		tokens = []
		level = self.trie
		begin = end = 0
		length = len(string)
		while begin < length:
			if re.match(ignore,string[begin]):
				begin+=1
				end = begin
				continue
			while level and level != {} and end < length:
				char = string[end]
				node = level.get(char, False)
				while not node and re.match(ignore, char) and end<length-1:
					end+=1
					char = string[end]
					node = level.get(char,False)
				if node==1:
					node = self.db.get(string[begin:end])
				if node:
					toks = node.get("to",[])
					if len(toks)>0:
						suffix = end
						while suffix+1<length and re.match(ignore, string[suffix+1]):
							suffix += 1
							
						for toki in toks:
							if len(toki)>2:
								pop = toki[2]
							else:
								pop = 1
								toki.append(1)
							tokens.append(symbol(toki[0], toki[1], [begin, suffix+1], pop));
						
				level = node
				end+=1
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
				if holes[h]==0 and h==len(holes)-1:
					h_spans.append(h+1)
				if holes[h]==1 and h!=0 and holes[h-1]==0:
					h_spans.append(h)
			
			returns = [symbol("hole",st[h_spans[i]:h_spans[i+1]],[h_spans[i],h_spans[i+1]]) 
						for i in range(0,len(h_spans),2) 
						if re.match(".*[A-Za-z]+.*",st[h_spans[i]:h_spans[i+1]])]
			tok.extend(returns)
			return tok
				
		tokens = post_tokenize(string, tokens)
		#print tokens
		return tokens
