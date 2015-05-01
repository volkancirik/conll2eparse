#!/usr/bin/env python
from __future__ import with_statement
import sys
import logging
__author__ = 'volkan cirik'


logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':
	import argparse

	parser = argparse.ArgumentParser(description='Create a clone of CoNLL corpus by adding pos tags as one-hot vectors', epilog="python %s conll conll_with_pos " % sys.argv[0])
	parser.add_argument('src', help="Root directory of CoNLL corpus to be used as source")
	parser.add_argument('target', help="Root directory of CoNLL corpus to be used as target")
	parser.add_argument('pos_column', action='store',help='pos column number , default 4',type=int,default = 4)
	parser.add_argument('delimiter', help="delimiter {space | tab}, default = space", default = "space")
	args = parser.parse_args()

	logging.info(str(args))

	import os

	delimiter = { "space" : ' ' , "tab" : '\t'}
	POS = {}
	NPOS = 0

	for dir in sorted(os.listdir(args.src)):
		for file in sorted(os.listdir("%s/%s" % (args.src, dir))):
			with open("%s/%s/%s" % (args.src, dir, file)) as fp:
				for line in fp:
					if len(line.strip()) == 0:
						continue
					tokens = line.strip().split('\t')
					if tokens[ args.pos_column ] not in POS:
						POS[tokens[ args.pos_column ]]	= NPOS 
						NPOS += 1

	logging.info("#of unique pos tags : %d", NPOS)
	for dir in sorted(os.listdir(args.src)):
		logging.info(dir)
		for file in sorted(os.listdir("%s/%s" % (args.src, dir))):
			logging.info("\t%s" % file)

			if not os.path.exists("%s/%s" % (args.target, dir)):
				os.makedirs("%s/%s" % (args.target, dir))

			with open("%s/%s/%s" % (args.src, dir, file)) as fp, open("%s/%s/%s" % (args.target, dir, file), "w") as wp:
				for line in fp:
					if len(line.strip()) == 0:
						print >> wp, ""
					else:
						tokens = line.strip().split('\t')
						pos_vec = [0]*NPOS
						pos_vec[ POS[tokens[ args.pos_column ]] ] = 1
						pos_vec = " ".join(str(v) for v in pos_vec )
						print >> wp, "%s%s%s" % (line.strip(), delimiter[args.delimiter],pos_vec)
