# explanations for member functions are provided in requirements.py
# each file that uses a Zip Tree should import it from this file.

from typing import TypeVar
from collections import deque
import random

KeyType = TypeVar('KeyType')
ValType = TypeVar('ValType')

class Node:
	key = None
	value = None
	rank = 0	
	def __init__(self, key: KeyType, value: ValType, rank: int):
		self.key = key
		self.value = value
		self.rank = rank
		self.left = None
		self.right = None

class ZipTree:			
	def __init__(self):
		self.root = None
		self.numNodes = 0

	@staticmethod
	def get_random_rank() -> int:
		rank = 0
		while True:
			rank += 1
			val = random.randint(1,2)
			if val == 1:
				return rank - 1

	def unzip(self, x:Node, y:Node):
		def unzip_lookup(key:KeyType, node:Node):
			if node is None:
				return None, None
			if node.key < key:
				p, q = unzip_lookup(key, node.right)
				node.right = p
				return node, q
			else:
				p, q = unzip_lookup(key, node.left)
				node.left = q
				return p, node
		return unzip_lookup(x.key, y)

	def getInsertNode(self, node: Node)-> Node:
		cur = self.root
		par = None
		while cur is not None:
			if cur.rank < node.rank:
				return par,cur
			elif cur.rank == node.rank and cur.key > node.key:
					return par, cur
			else:	
				par = cur			
				if cur.key > node.key:
					cur = cur.left
				else:
					cur = cur.right
		return par,None
		
	def insert(self, key: KeyType, val: ValType, rank: int = -1):
		self.numNodes += 1
		if rank == -1:
			rank = ZipTree.get_random_rank()
		node = Node(key, val, rank)
		
		if self.root is None:
			self.root = node			
		else:
			par, ins = self.getInsertNode(node)
			if ins is None:
				if par.key > key:
					par.left = node
				else:
					par.right = node
				return
			if par is None:
				p, q = self.unzip(node, ins)
				node.left = p
				node.right = q
				self.root = node
				return
			if par is not None:
				if par.key < node.key:
					par.right = node
				else:
					par.left = node
			p, q = self.unzip(node, ins)
			node.left = p
			node.right = q
					
		
	def zip(self, x: Node):
		def zipup(p: Node, q: Node):
			if p is None: return q
			if q is None: return p
			if q.rank > p.rank:
				q.left = zipup(p, q.left)
				return q
			else:
				p.right = zipup(p.right, q)
				return p
		return zipup(x.left, x.right)
	
	def remove(self, key: KeyType):
		self.numNodes -= 1
		cur = self.root
		par = None
		while cur is not None:
			if cur.key == key:
				break
			elif cur.key < key:
				par = cur
				cur = cur.right
			else:
				par = cur
				cur = cur.left
		node = self.zip(cur)
		if par is None:
			self.root = node
			return
		if par.key > cur.key:
			par.left = node
		else:
			par.right = node		

	def find(self, key: KeyType) -> ValType:
		node = self.root		
		while node.key != key:
			if node.key > key:
				node = node.left
			else:
				node = node.right			
		return node.value


	def get_size(self) -> int:
		return self.numNodes

	def get_height(self) -> int:					
		q = [self.root]				
		ht = 0
		while q:									
			ht += 1
			for _ in range(len(q)):
				node = q.pop(0)								
				if node.left != None:					
					q.append(node.left)
				if node.right != None:					
					q.append(node.right)
		return ht - 1

	def get_depth(self, key: KeyType):
		node = self.root
		depth = 0
		while node.key != key:
			if node.key > key:
				node = node.left
			else:
				node = node.right
			depth += 1
		return depth

# feel free to define new classes/methods in addition to the above
# fill in the definitions of each required member function (above),
# and any additional member functions you define
