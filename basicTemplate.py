#!/usr/bin/python


'''
-dependencies
-functions
-classes
-main
	-instantiated classes, instances, global variables
'''



#dependencies
import argparse

#functions

def main():
	parser = argparse.ArgumentParser(description="Template script tool")
	parser.add_argument('-f', help='takes arbitrary input')
	parser.add_argument('-b', action='store_true', help='binary flag')
	args=parser.parse_args()

class nullExample:	

	def __init__(self):
		internalVar='hello'

	def bar(self):
		print self.internalVar

class example():

        def __init__(self,var):
                self.internalVar=var



if __name__ == "__main__":
	foo = nullExample()
	bar = example('arbitrary object/value/pointer')
        main()
