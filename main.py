# Check the ASCII code of the character
def isPrintable(character) :
	if ((character >= 65 and character <= 90) 		# Upper case letter
		or (character >= 97 and character <= 122)	# Lower case letter
		or character == 44 or character == 46 or character == 39		# Classical punctuation
		or character == 32) :				# space
		return True
	return False 

# First, parse the dictionary file !  print("Parse dictionary ...")
dico = {} 
fd = open("wordsEn.txt", "r")
print("Parse dictionary ..")
for line in fd:
	cur = dico
	for letter in line:
		code = ord(letter) 	# Process faster with numbers
		if code == 10:		# newline : "\n"
			continue
		if (not code in cur) :
			cur[code] = {}
		cur = cur[code]
	cur[32] = 1			# Don't forget the space !
print("Done")

import messages as mes
# The messages list must not be empty !

# The size of the bigger message
# (Will be the length of the key we are looking for ..)
longestSize = len(mes.messages[0])
for e in mes.messages :
	if len(e) > longestSize:
		longestSize = len(e)


# Every possible keys (It is a two-dimensions list)
# As and when the execution of the program, strip this list to only 
# keep the "possible" keys (i.e. the ones that generates printable 
# characters and real words).
# At the end, it must only remains the real key ..
key = []
decrypt = []

# First, only keep the key-bytes that produce printable characters ..
# (Printable characters include letters (lower and upper case,
# punctuation and spaces).
for i in xrange(longestSize) :
	key.append([])
	decrypt.append([])
	for byte in xrange(255):
		printable = True
		decryptBytes = {}
		for m in xrange(len(mes.messages)) :
			if len(mes.messages[m]) > i :
				msgByte = mes.messages[m][i]
				if (not isPrintable(msgByte ^ byte)) :
					printable = False
					break
				decryptBytes[m] = msgByte ^ byte;
		if printable:
			key[i].append(byte)
			decrypt[i].append(decryptBytes)


# One list per message.
# Each list contains a dictionary of possible sentences (associated
# with the corresponding key used to find these sentences)
words = []

def makeWord(msgId, offset, currentWord, dicoPosition, wordLength):
	global key
	global decrypt
	global words
	global dico
	if(offset >= len(mes.messages[msgId])):
		print(currentWord + " ..................")
		return 0
	for i in xrange(len(key[offset])) :
		character = decrypt[offset][i][msgId]
		if (character >= 65 and character <= 90) : # Change to lower case if needed		
			character = character + 32
		elif character in (32, 44, 46, 39) : 	# Word separator
			character = 32			# Space
		if character in dicoPosition :
			if character == 32:
				print(currentWord + str(msgId))
				makeWord(msgId, offset + 1, currentWord + chr(decrypt[offset][i][msgId]), dico, 0)
			else:
				makeWord(msgId, offset + 1, currentWord + chr(character), dicoPosition[character], wordLength + 1)
			

# Now, try to find the first word
for k in xrange(len(mes.messages)) :
	makeWord(k, 0, "", dico, 0)
