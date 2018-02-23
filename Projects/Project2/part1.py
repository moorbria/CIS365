import sys
import re
import math

totalWords = 0
totalSentences = 0
totalSyllables = 0
syllablesDict = {}
misses = 0
for arg in sys.argv:
	print(arg)


if len(sys.argv) != 2:
	print("Invalid number of arguments, please type a single filename")
	sys.exit(2)

s = open("Syllables.txt", encoding='utf-8', mode='r')

# Set up Syllables Dictionary
for line in s:
	syllablesDict[line.split("=")[0]] = len(line.split("=")[1].split("+"))

# Open file for wordcount
file_tmp = open(sys.argv[1], 'r')
word_count = len(file_tmp.read().split())

# Open file again for line parsing
f = open(sys.argv[1], 'r')
words = ""

# Parse each line
for line in f:

	# Calculate number of sentences
	totalSentences += (len(re.split(r'[.?!]\s*', line)) - 1)
	line = re.sub('[^0-9a-zA-Z]+', ' ', line) 
	for word in line.split():
		wordFound = True
		word = word.lower()
		word = re.sub('[^A-Za-z0-9]+', '', word) # Removes puncuations

		try:
			if len(word) < 4:
				totalSyllables += 1
			else:	
				#print(word + ":" + str(syllablesDict[word]))
				totalSyllables += syllablesDict[word]
		except KeyError:
			wordFound = False	

		if not wordFound:
			try:
				# Example: churches -> church
				if word.endswith("es") and syllablesDict.get(word[:-2]) is not None:
					#print("Removing 'es' from " + word)
					#print("Adding 1 syllable")
					#print(word + ":" + str(syllablesDict[word[:-2]]))
					totalSyllables += syllablesDict[word[:-2]] + 1
				# Example: programs -> program
				elif word.endswith("s") and syllablesDict.get(word[:-1]) is not None:
					#print("Removing 's' from " + word)
					#print(word + ":" + str(syllablesDict[word[:-1]]))
					totalSyllables += syllablesDict[word[:-1]]
				# Example: thinking -> think 
				elif word.endswith("ing") and syllablesDict.get(word[:-3]) is not None:
					#print("Removing 'ing' from " + word)
					#print("Adding 1 syllable")
					#print(word + ":" + str(syllablesDict[word[:-3]]))
					totalSyllables += syllablesDict[word[:-3]] + 1
				# Example: dancing -> dance 
				elif word.endswith("ing") and syllablesDict.get(word[:-3] + 'e') is not None:
					#print("Removing 'ing' from " + word)
					#print("Adding 1 syllable")
					#print(word + ":" + str(syllablesDict[word[:-3] + 'e']))
					totalSyllables += syllablesDict[word[:-3] + 'e'] + 1
				# Example: running -> run 
				elif word.endswith("ing") and syllablesDict.get(word[:-4]) is not None:
					#print("Removing 'ing' from " + word)
					#print("Adding 1 syllable")
					#print(word + ":" + str(syllablesDict[word[:-4]]))
					totalSyllables += syllablesDict[word[:-4]] + 1
				# Example: paged -> page 
				elif word.endswith("ed") and syllablesDict.get(word[:-1]) is not None:
					#print("Removing 'd' from " + word)
					#print(word + ":" + str(syllablesDict[word[:-1]]))
					totalSyllables += syllablesDict[word[:-1]]
				# Example: yelled -> yell 
				elif word.endswith("ed") and syllablesDict.get(word[:-2]) is not None:
					#print("Removing 'ed' from " + word)
					#print(word + ":" + str(syllablesDict[word[:-2]]))
					totalSyllables += syllablesDict[word[:-2]]
				# Example: dropped -> drop 
				elif word.endswith("ed") and syllablesDict.get(word[:-3]) is not None:
					#print("Removing 'ed' from " + word)
					#print(word + ":" + str(syllablesDict[word[:-3]]))
					totalSyllables += syllablesDict[word[:-3]]
				# Example: rarer -> rare
				elif word.endswith("er") and syllablesDict.get(word[:-1]) is not None:
					#print("Removing 'r' from " + word)
					#print(word + ":" + str(syllablesDict[word[:-1]]))
					totalSyllables += syllablesDict[word[:-1]] + 1
				# Example: drinker -> drink 
				elif word.endswith("er") and syllablesDict.get(word[:-2]) is not None:
					#print("Removing 'er' from " + word)
					#print(word + ":" + str(syllablesDict[word[:-2]]))
					totalSyllables += syllablesDict[word[:-2]]
				# Example: thinner -> thin 
				elif word.endswith("er") and syllablesDict.get(word[:-3]) is not None:
					#print("Removing '[x]er' from " + word)
					#print(word + ":" + str(syllablesDict[word[:-3]]))
					totalSyllables += syllablesDict[word[:-3]] + 1
				# Example: bunnies -> bunny 
				elif word.endswith("ies") and syllablesDict.get(word[:-3] + 'y') is not None:
					#print("Removing 'ies' from " + word)
					#print(word + ":" + str(syllablesDict[word[:-3] + 'y']))
					totalSyllables += syllablesDict[word[:-3] + 'y']
				# Example: triumphantly -> triumphant 
				elif word.endswith("ly") and syllablesDict.get(word[:-2]) is not None:
					#print("Removing 'ly' from " + word)
					#print(word + ":" + str(syllablesDict[word[:-2]]))
					totalSyllables += syllablesDict[word[:-2]] + 1
				# Example: simplest -> simple 
				elif word.endswith("est") and syllablesDict.get(word[:-2]) is not None:
					#print("Removing 'est' from " + word)
					#print(word + ":" + str(syllablesDict[word[:-2]]))
					totalSyllables += syllablesDict[word[:-2]] + 1
				# Example: lowest -> low 
				elif word.endswith("est") and syllablesDict.get(word[:-3]) is not None:
					#print("Removing 'est' from " + word)
					#print(word + ":" + str(syllablesDict[word[:-3]]))
					totalSyllables += syllablesDict[word[:-3]] + 1
				# Example: 
				elif word.endswith("ness") and syllablesDict.get(word[:-4]) is not None:
					#print("Removing 'ed' from " + word)
					#print(word + ":" + str(syllablesDict[word[:-4]]))
					totalSyllables += syllablesDict[word[:-4]] + 1
				# Example: 
				elif word.endswith("ed") and syllablesDict.get(word[:-2]) is not None:
					#print("Removing 'ed' from " + word)
					#print(word + ":" + str(syllablesDict[word[:-2]]))
					totalSyllables += syllablesDict[word[:-2]]
				# Example: 
				else:
					raise KeyError
			except KeyError:
				#print("Making up syllable count"+ str(math.ceil(len(word)/4)))
				totalSyllables += math.ceil(len(word)/3)
				#print("Making up syllable count"+ str(math.ceil(len(word)/4)))
				misses += 1
				words += word + " "
				#print("Key: '" + word + "' not found")

readability = 206.835 - 1.015 * (totalWords/totalSentences) - 84.6 * (totalSyllables/word_count)

if totalSentences == 0 and word_count > 0:
	totalSentences = 1

#print("Missed words:" + words)
#print("Misses: " + str(misses))
print("Words: " + str(word_count))
print("Total Syllables: " + str(totalSyllables))
print("Total Sentences: " + str(totalSentences))
print("Readability: " + str(readability))
