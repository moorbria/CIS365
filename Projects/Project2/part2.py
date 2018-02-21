import sys
import re

print("Num args" + str(len(sys.argv)))
for arg in sys.argv:
	print(arg)


if len(sys.argv) != 2:
	print("Invalid number of arguments, please type a single filename")
	sys.exit(2)


in_file = open(sys.argv[1], 'r')
out_file = open("outfile.log", 'w')

for line in in_file:
	#print(line, end='')
	for word in line.split():
		#word = word.lower()
		#word = re.sub('[^A-Za-z0-9]+', '', word) # Removes puncuations
		print(word)	
		
		# do some word manipulation here 
		# Ex: Remove 'ing' from the end of words (jumping -> jump)
		
		out_file.write(word)
		out_file.write(" ")
	out_file.write("\n")
in_file.close()
out_file.close()

