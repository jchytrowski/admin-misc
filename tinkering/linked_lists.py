#!/usr/bin/python

#motivation; it's been a while since i've fiddled with linked lists, lets see if i've still got it.

class linked_list:
	head=None
	tail=None
	def __init__(self):
		head=None
		tail=None

	def unsorted_append(self,node):

		if self.head is None:
			self.head=node
			self.tail=node

		elif self.tail is not None:
			tmp=self.tail
			tmp.set_next(node)
			self.tail=node

	def sorted_append(self,node):
		if self.head is None:
			self.head=node
			self.tail=node
			return None	

		else:
			prev=self.head
			curr=self.head
			while curr is not None:
				if node.data < curr.data and curr == self.head:
					tmp=curr
					self.head=node
					node.set_next(tmp)
					return
				elif node.data < curr.data:
					prev.set_next(node)
					node.set_next(curr)
					return
				elif curr.snext is None:
					curr.set_next(node)
					return
				else:
					curr=curr.snext

	def print_list(self):
		curr=self.head
		while curr is not None:
			print curr.data
			curr=curr.snext


class node:
	data=None
	snext=None
	#sprev=None

	def __init__(self,data):
		self.data=data
		self.snext=None
		#self.sprev=self

	def set_next(self,node):
		self.snext=(node)


test=linked_list()


test.unsorted_append(node('z'))
test.unsorted_append(node('b'))
test.sorted_append(node('c'))
test.sorted_append(node('d'))
test.unsorted_append(node('a'))

resort=linked_list()

test_list=test.print_list()



print test_list

#for entry in test.print_list():
#	resort.sorted_append(node(entry))

#test.print_list()
#resort.print_list()
