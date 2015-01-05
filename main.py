longestSize = 0
longestIndex = 0
wordMaxLength = 0

# Check the ASCII code of the character
def isPrintable(character) :
	if ((character >= 65 and character <= 90) 		# Upper case letter
		or (character >= 97 and character <= 122)	# Lower case letter
		or character == 44 or character == 46 or character == 39		# Classical punctuation
		or character == 32) :				# space
		return True
	return False 

# Return True if pattern in tab (Including the offsets) 
def tabMatch(tab, pattern, tabOffset, patternOffset, length): 
	for i in xrange(length): 
		if tab[i + tabOffset] != pattern[i + patternOffset]:
			return False
	return True

# grid is expected to be a non-empty 3D list
# This function returns the common value of this level (x) : [][x][index - length]
# (If several are found, it returns the first one)
def findIntersection(grid, index, length):
	global longestIndex
	global foundWords
	# We take the longest message as a reference, but it could very well be another.
	for patternRaw in grid[longestIndex]:
		pattern = patternRaw[index:(index+length)]
		print(longestIndex, "pattern : ", pattern, index, len(grid))
		# We now check if this pattern is present in the other messages
		presentInAll = True
		for i in xrange(0, len(grid)):
			print("Len : ", len(grid[i]))
			if (i == longestIndex) :				# Don't process the reference
				continue
			if(len(grid[i][0]) <= index):			# We skip messages that have been completely uncrypted ..
				print("SKIP ", i)
				continue
			patternMatches = 0 		# Number of time the pattern is present
			#if len(grid[i]) == 1:		# If there is only one possibility remaining, we keep going on it
			#	patternMatches = 1
			for word in grid[i]:
				present = tabMatch(word, pattern, index, 0, length)
				if present: 
					print(i, "IN ", len(word))
					patternMatches += 1
					break
				else:
					print(i, "not in ", len(word))
			if (patternMatches == 0):	# It MUST be present in every messages
				presentInAll = False
				#print("BREAK")
				break
		if presentInAll:
			return pattern
	print("No common parts !") # At least in the first message ..
	print(grid)
	return []

# First, parse the dictionary file !  
dico = {} 
fd = open("wordsEn.txt", "r")
print("Parse dictionary ..")
for line in fd:
	if(len(line) > wordMaxLength):
		wordMaxLength = len(line)
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
for i in xrange(len(mes.messages)) :
	if len(mes.messages[i]) > longestSize:
		longestSize = len(mes.messages[i])
		longestIndex = i

def printMessage(msgId, key):
	message = ""
	for i in xrange(2, key[1] + 2):
		message += chr(mes.messages[msgId][i - 2] ^ key[i])
	print(message)

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
		
print(key[8])


# One list per message.
# Each list contains a dictionary of possible sentences (associated
# with the corresponding key used to find these sentences)
words = []

def makeWord(msgId, offset, currentWord, dicoPosition, wordLength):
	global key
	global decrypt
	global words
	global dico
	global wordMaxLength
	if(offset >= len(mes.messages[msgId])):
		if(msgId == 9): print("ENNNNNNND")
		return -1
	#if(wordLength > wordMaxLength + 2):
	#	return -1
	possibilities = []
	for i in xrange(len(key[offset])) :
		character = decrypt[offset][i][msgId]
		if(msgId == 9): print("offset ", offset, chr(character))
		if(msgId == 9 and character == 46):
			print("YOUPI")
		if (character >= 65 and character <= 90) : # Change to lower case if needed		
			character = character + 32
		elif character in (32, 44, 46, 39) : 	# Word separator
			character = 32			# Space
		if character in dicoPosition :
			if character == 32:
				# The first cell of each words stores the word's offset in the message
				possibilities.append([offset, wordLength + 1] + currentWord + [key[offset][i]])
			else:
				possibilities.extend(makeWord(msgId, offset + 1, currentWord + [key[offset][i]], dicoPosition[character], wordLength + 1))
	return possibilities

def extendWord(msgId, currentWord):
	global dico
	currentLength = currentWord[1]
	currentOffset = currentWord[0]
	nextPossibilities = makeWord(msgId, currentOffset + 1, [], dico, 0)
	if(nextPossibilities == -1):	# We reach the end of the message ..
		return -1
	nextWords = []
	for pos in nextPossibilities:
		nextWord = [pos[0], currentLength + pos[1]] + currentWord[2:] + pos[2:]
		nextWords.append(nextWord)
	return nextWords

# Now, get every possibilities for the first word
# (By the way, it initialize the words list)
for k in xrange(len(mes.messages)) :
	words.append(makeWord(k, 0, [], dico, 0))

# i is the index in the key
i = 0
previous = (0, 0)
foundKey = []
foundWords = [] 	# The words that we completely found
while i < longestSize:
	shortestWord = wordMaxLength + 10
	for j in xrange(len(words)):		#len(words) is the number of messages
		newWords = []
		if j in foundWords:
			newWords.append(words[j][0])	# Else, add the word to avoid out of range exception
			continue
		# First, make sure this word passed the previous loop (i.e. match the begining of the found key)
		# Then, make sure we have enough characters ..
		for word in words[j]:
			if (tabMatch(word, foundKey, previous[0] + 2, previous[0], previous[1])):
				if word[1] <= i:	# Remember, the second cell is the word length
					if(j == 9):
						printMessage(j, word)
					extension = extendWord(j, word)
					if(extension != -1):		# If it is -1, the message has been completely found
						if(j == 9):
							print("extend", extension)
						newWords.extend(extension)
					else:
						foundWords.append(j)
						newWords.append(word)
				else:
					newWords.append(word)
		words[j] = newWords
		for word in words[j]:
			if (word[1] - i < shortestWord): 	# This value depend on the current offset (i) ! 
				shortestWord = word[1] - i
	foundKey.extend(findIntersection(words, i + 2, shortestWord))
	previous = (i, shortestWord)
	i += shortestWord
	print(i)
			
print(foundKey)
