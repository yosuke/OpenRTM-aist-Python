#!/usr/bin/env python
# -*- Python -*-

class HOGE:
    def __init__(self):
        pass

def echo(*args):
    print "hello HOGE"

        

"""
import sys
argv = sys.argv[1:]
for x in argv:
	try:
		f = open(x)
		print"---",x,"---"
		for i in range(15):
			print i+1,f.readline(),
		print "---",x,"---\n"
		f.close()
	except IOError:
		print "Can't find file:", x		

"""

		
