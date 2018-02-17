import sys
import re
import math

totalWords = 0
totalSentences = 0
totalSyllables = 0
syllablesDict = {}
misses = 0
print("Num args" + str(len(sys.argv)))
for arg in sys.argv:
	print(arg)


if len(sys.argv) != 2:
	print("Invalid number of arguments, please type a single filename")
	sys.exit(2)

s = open("Syllables.txt", encoding='utf-8', mode='r')

for line in s:
#	print(line, end='')
	syllablesDict[line.split("=")[0]] = len(line.split("=")[1].split("+"))

#print(syllablesDict)
#f = open(sys.argv[1], encoding='utf-8', mode='r')
f = open(sys.argv[1], 'r')
words = ""
#print(syllablesDict['the'])
for line in f:
	#print(line, end='')
	totalSentences += len(re.split(r'[.?!]\s*', line))	
	line = re.sub('[^0-9a-zA-Z]+', ' ', line) 
	for word in line.split():
		totalWords += 1
		#word = word.replace('\ufeff', "")
		word = word.lower()
		word = re.sub('[^A-Za-z0-9]+', '', word) # Removes puncuations
		

		try:
			if len(word) < 4:
				totalSyllables += 1
			else:	
				print(word + ":" + str(syllablesDict[word]))
				totalSyllables += syllablesDict[word]
		except KeyError:
			try:
				if word.endswith("es") and syllablesDict.get(word[:-2]) is not None:
					print("Removing 'es' from " + word)
					print("Adding 1 syllable")
					print(word + ":" + str(syllablesDict[word[:-2]]))
					totalSyllables += syllablesDict[word[:-2]] + 1
				elif word.endswith("s")and syllablesDict.get(word[:-1]) is not None:
					print("Removing 's' from " + word)
					print(word + ":" + str(syllablesDict[word[:-1]]))
					totalSyllables += syllablesDict[word[:-1]]
				elif word.endswith("ing")and syllablesDict.get(word[:-3]) is not None:
					print("Removing 'ing' from " + word)
					print("Adding 1 syllable")
					print(word + ":" + str(syllablesDict[word[:-3]]))
					totalSyllables += syllablesDict[word[:-3]] + 1
				elif word.endswith("ed")and syllablesDict.get(word[:-1]) is not None:
					print("Removing 'd' from " + word)
					print(word + ":" + str(syllablesDict[word[:-1]]))
					totalSyllables += syllablesDict[word[:-1]]
				elif word.endswith("ed")and syllablesDict.get(word[:-2]) is not None:
					print("Removing 'ed' from " + word)
					words += word + " "
					print(word + ":" + str(syllablesDict[word[:-2]]))
					totalSyllables += syllablesDict[word[:-2]]
			except KeyError:
				totalSyllables += math.ceil(len(word)/4)
				print("Making up syllable count"+ str(math.ceil(len(word)/4)))
				misses += 1
				print("Key: '" + word + "' not found")
readability = 206.835 - 1.015 * (totalWords/totalSentences) - 84.6 * (totalSyllables/totalWords)

print("Misses: " + str(misses))
print("Words: " + str(totalWords))
print("Total Syllables: " + str(totalSyllables))
print("Total Sentences: " + str(totalSentences))
print("Readability: " + str(readability))
