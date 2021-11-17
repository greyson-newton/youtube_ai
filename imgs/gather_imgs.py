import os
# First, you're going to need to import wordnet:
from nltk.corpus import wordnet
# Then, we're going to use the term "program" to find synsets like so:
# syns = wordnet.synsets("program")
with open("places_search_terms.txt","r") as outf:
	for l in outf:
		if '\n' in l:
			l=l.replace('\n','')
		if '(' in l:
			l=l.replace('(','')
		if ')' in l:
			l=l.replace(')','')
		command="python bbid.py -s '"+l +"' -o ./imgoutput/"+l
		print("--------------",l,"--------------")
		print(command)
		os.system(command)
		
		print("---------------------------------")