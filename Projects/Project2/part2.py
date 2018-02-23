import sys
import re
import nltk
from nltk.corpus import wordnet

print("Num args" + str(len(sys.argv)))
for arg in sys.argv:
	print(arg)


if len(sys.argv) != 2:
	print("Invalid number of arguments, please type a single filename")
	sys.exit(2)


#Opening files
in_file = open(sys.argv[1], 'r', encoding='utf-8')
INCout_file = open("IncreasedReadingLevel.txt", 'w', encoding='utf-8')
REDout_file = open("DecreasedReadingLevel.txt", 'w', encoding='utf-8')

#list of words that can be eliminated and hopefully not change the readability 
trash = ["little", "a little", "very", "Very", "Just", "just", "sort of", "kind of",
		"at most", "at least", "a lot"]


#Method to reduce the reading level of a word
def reduceReadingLevel(word): 
	synonyms = []
	antonyms = []
	#word = word.lower()
	#word = re.sub('[^A-Za-z0-9]+', '', word) # Removes puncuations
	print(word)	
	
	#if the length of the word is greater than 6, we want to look at the words synonyms for a shorter word and replace it with our current word
	if len(word) >= 6:
		#if the word has a period at the end, we need to check for synonyms of just that word, so we remove the period and add it back in at the end.
		if word.endswith("."):
			#getting synonyms
			for syn in wordnet.synsets(word[:-1]):
				for l in syn.lemmas():
					synonyms.append(l.name())
					#sorting the synonym list by length of word
					synonyms.sort(key = len)
					#setting the word to the shortest synonym 
					word = synonyms[0] + "."

			"""for ss in wordnet.synsets(word[:-1]):
				synonyms.append(ss.lemma_names())
				synonyms.sort(key = len)
				word = synonyms[0]"""				
		else:
			#getting synonyms
			for syn in wordnet.synsets(word):
				for l in syn.lemmas():
					synonyms.append(l.name())
					#sorting the synonym list by length of word
					synonyms.sort(key = len)
					#setting the word to the shortest synonym 
					word = synonyms[0]

			"""for ss in wordnet.synsets(word):
				synonyms.append(ss.lemma_names())
				synonyms.sort(key = len)
				word = synonyms[0]"""

	# do some word manipulation here 
	# Ex: Remove 'ing' from the end of words (jumping -> jump)

	#if the word is in our trash list, we delete it
	if word in trash:
		word = ""

	#if the word ends with ly we delete it
	elif word.endswith("ly"):
		word = ""
	#if the word ends with a comma, we replace it with a period
	elif word.endswith(","):
		word = word[:-1]
		word = word + "."
		print("changed: " + word)
	#if the word ends with ing, we remove the ing
	elif word.endswith("ing"):
		word = word[:-3]
		print(word)

	#print(synonyms)
	print(word)
	#print(set(antonyms))
	
	#write the word to file
	REDout_file.write(word)
	REDout_file.write(" ")

#Method to increase the reading level of a word
def increaseReadingLevel(word):
	synonyms = []
	antonyms = []
	#word = word.lower()
	#word = re.sub('[^A-Za-z0-9]+', '', word) # Removes puncuations
	print(word)	
	
	#We want to look for more complex synonyms of every word
	if len(word) >= 0:
		#if the word has a period at the end, we need to check for synonyms of just that word, so we remove the period and add it back in at the end.
		if word.endswith("."):
			for syn in wordnet.synsets(word[:-1]):
				for l in syn.lemmas():
					synonyms.append(l.name())
					synonyms.sort(key = len, reverse=True)
					word = synonyms[0] + "."

			"""for ss in wordnet.synsets(word[:-1]):
				synonyms.append(ss.lemma_names())
				synonyms.sort(key = len)
				word = synonyms[0]"""				
		else:
			for syn in wordnet.synsets(word):
				for l in syn.lemmas():
					synonyms.append(l.name())
					synonyms.sort(key = len, reverse = True)
					word = synonyms[0]

			"""for ss in wordnet.synsets(word):
				synonyms.append(ss.lemma_names())
				synonyms.sort(key = len)
				word = synonyms[0]"""

	#print(synonyms)
	print(word)
	#print(set(antonyms))
	INCout_file.write(word)
	INCout_file.write(" ")

synonyms = []
antonyms = []

#Checking every line in the file for phrases in the trash list and removing them
for line in in_file:
	for t in trash:
		if t in line:
			line = line.replace(t, "")
	#print(line, end='')
	for word in line.split():
		increaseReadingLevel(word)
		reduceReadingLevel(word)

	#out_file.write(lineout)
	REDout_file.write("\n")
	INCout_file.write("\n")

in_file.close()
REDout_file.close()
INCout_file.close()