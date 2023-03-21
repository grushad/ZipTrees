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
	numNodes = 0
	def __init__(self):
		self.root = None

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

	def getInsertNode(self, node: Node, cur: Node, par: Node)-> Node:
		if cur is None:
			return cur, par
		if cur.rank < node.rank:
			return cur, par
		if cur.rank == node.rank:
			if cur.key > node.key:
				return cur, par
			else:
				return self.getInsertNode(node, cur.right, cur)
		if cur.key > node.key:
			return self.getInsertNode(node, cur.left, cur)
		else:
			return self.getInsertNode(node, cur.right, cur)
		
		
	def insert(self, key: KeyType, val: ValType, rank: int = -1):
		if rank == -1:
			rank = ZipTree.get_random_rank()
		node = Node(key, val, rank)
		
		if self.root is None:
			self.root = node
		else:
			y, par = self.getInsertNode(node, self.root, self.root)
			p, q = self.unzip(node, y)
			node.left = p
			node.right = q
			if par.key < node.key:
				par.right = node
			else:
				par.left = node
		self.numNodes += 1
		
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
		#self.inorder(self.root)	
		node = self.root
		if node is None or (node.left is None and node.right is None):
			return 0
		q = deque()		
		q.append(node)
		ht = 0
		while q:			
			sz = len(q)
			#print("height" + str(sz) + " " + str(ht))
			ht += 1
			for i in range(sz):
				node = q.popleft()								
				if node.left is not None:
					# print(node.left)
					q.append(node.left)
				if node.right is not None:
					# print(node.right)
					q.append(node.right)
		return ht - 1

	def inorder(self, node:Node):
		if node is None:
			return
		self.inorder(node.left)
		print(node.value)
		self.inorder(node.right)


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
