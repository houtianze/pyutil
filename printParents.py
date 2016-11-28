from types import *

# https://stackoverflow.com/questions/2611892/get-python-class-parents
def printParents(thing, ident = 2):
	'''
	Print out all the parents (till the ancestors) of a given class / object.
	@param indent: Print indentation
	'''
	typ = type(thing)
	if typ is ClassType:
		printClassParents(thing, 0)
	elif typ is InstanceType:
		print("Object: {}".format(thing))
		printClassParents(thing.__class__, 0)
	else:
		print("'{}' - '{}'".format(thing, type))
		print("I don't know your parents.")

def printClassParents(cls, level = 0, indent = 2):
	thisLevel = ' ' * indent * level + "{} --> {{ {} }}".format(
		cls, ', '.join(str(c) for c in cls.__bases__))
	print(thisLevel)
	for base in cls.__bases__:
		printClassParents(base, level + 1)

if __name__ == '__main__':
	import sys

	def help(names):
		print("Invalid arg: {}\nSyntax: modeul1.class1 module2.class2".format(names))

	if len(sys.argv) > 1:
		# input args: module1.class1 module2.class2 ...
		# eg. printParents.py Tkinter.Frame Tkinker.Button
		# https://stackoverflow.com/questions/4821104/python-dynamic-instantiation-from-string-name-of-a-class-in-dynamically-imported
		for names in sys.argv[1:]:
			mc = names.split('.')
			if len(mc) == 2:
				# price you pay when you go dynamic
				try:
					ctor = getattr(__import__(mc[0]), mc[1])
					inst = ctor()
					printParents(inst)
					print('=' * 32)
				except:
					help(names)
			else:
				help(names)
	else:	
		from ttk import *
		button = Button()
		printParents(button)
		print('=' * 32)
		printParents(Label)
		print('=' * 32)
		printParents(8)
