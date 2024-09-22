"""
This is a program that encrypts and decrypts messages using a custom alphabet and a scrambling phrase.
The program uses a dictionary to store pairs of letters and their encrypted counterparts, and a function to encrypt and decrypt messages.
The program also includes a function to find possible decryptions of a message, given a scrambled message and a key.
"""

KB_ALPHABET = "qwertyuiopasdfghjklzxcvbnm"
ALPHABET = "abcdefghijklmnopqrstuvwxyz"
NUMBERS = "1234567890"

f = open("words.txt")
wordlist = set(i.lower() for i in f.read().split('\n'))

def encrypt(phraseToScramble: str) -> str:
    """
    This function encrypts a message using a custom alphabet and a scrambling phrase.
    The function first converts the message to lowercase and removes any non-alphabetic characters.
    It then reverses the scrambling phrase and creates a new string of letters from the scrambled phrase.
    The function then iterates through the original message, and for each letter in the message,
    it finds the corresponding letter in the scrambling phrase.
    It then adds the index of the letter in the scrambling phrase to the index of the letter in the
    original message, and takes the modulus of the result with 26.
    The function then adds the corresponding letter from the custom alphabet to the encrypted message.
    If the letter is not in the custom alphabet, it is added to the encrypted message as is.
    """
    encrypted = ""
    scrambleIndex = 0
    phraseToScramble = phraseToScramble.lower()
    phraseToScramble = [i for i in phraseToScramble if i in (ALPHABET + " ")]
    scramblingPhrase = [i for i in phraseToScramble[::-1] if i != " "]

    for i in phraseToScramble:
        if i in ALPHABET:
            encrypted += KB_ALPHABET[
                (
                    KB_ALPHABET.index(i)
                    + ALPHABET.index(scramblingPhrase[scrambleIndex])
                    + 1
                )
                % 26
            ]
            scrambleIndex += 1
        else:
            encrypted += i

    return encrypted


# Replacing the nested loops with a dictionary comprehension for efficiency
pairMatches = {i + j: [] for i in ALPHABET for j in ALPHABET}
# Using a single loop to populate pairMatches
for pair in (i + j for i in ALPHABET for j in ALPHABET):
    pairMatches[encrypt(pair)].append(pair)


def decrypt(encrypted: str) -> tuple[str, list[tuple[str, list[str]]]]:
    """
    This function decrypts a message using a custom alphabet and a scrambling phrase.
    The function first converts the message to lowercase and removes any non-alphabetic characters.
    It then reverses the scrambling phrase and creates a new string of letters from the scrambled phrase.
    The function then iterates through the original message, and for each letter in the message, it finds the corresponding letter in the scrambling phrase.
    It then adds the index of the letter in the scrambling phrase to the index of the letter in the original message, and takes the modulus of the result with 26.
    The function then adds the corresponding letter from the custom alphabet to the encrypted message.
    If the letter is not in the custom alphabet, it is added to the encrypted message as is.
    """
    decrypted = [" " for i in encrypted]
    nospaces = [i for i in encrypted if i != " "]
    decryptedletters = ["" for i in nospaces]
    unsureCount = 1
    unsureList = []
    half = int(len(nospaces) / 2)
    if len(nospaces) % 2 == 1:
        half += 1

    for i in range(half):
        pair = nospaces[i] + nospaces[-i - 1]
        if len(pairMatches[pair]) == 1:
            decryptedletters[i] = pairMatches[pair][0][0]
            decryptedletters[-i - 1] = pairMatches[pair][0][1]
        elif len(pairMatches[pair]) > 1:
            decryptedletters[i] = str(unsureCount)
            decryptedletters[-i - 1] = str(unsureCount)
            unsureList.append((unsureCount, pairMatches[pair]))
            unsureCount += 1
            unsureCount = unsureCount % 10

    j = 0
    for i in range(len(decrypted)):
        if encrypted[i] != " ":
            decrypted[i] = decryptedletters[j]
            j += 1

    decrypted = "".join(decrypted)
    return (decrypted, unsureList)


def findPossibles(
    nospaces: list[str], key: list[tuple[str, list[str]]], possibles: list[str]
) -> list[list[str]]:
    """
    This function finds all possible decryptions of a message, given a scrambled message and a key.
    The function first creates a list of possible decryptions for each pair of letters in the scrambled message.
    It then iterates through the list of possible decryptions, and for each possible decryption, it checks if it is a valid decryption.
    If it is, it adds the possible decryption to the list of possible decryptions.
    """
    possible = nospaces[:]  # create copy of nospaces
    half = int(len(nospaces) / 2)
    if len(nospaces) % 2 == 1:
        half += 1

    for i in range(half):
        if nospaces[i] in NUMBERS:
            for j in key[0][1]:
                possible[i] = j[0]
                possible[-i - 1] = j[1]
                if len(key) == 1:
                    possibles.append([i for i in possible])
                else:
                    findPossibles(possible, key[1:], possibles)

    return possibles


def givePossibles(decrypted: tuple[str, list[tuple[str, list[str]]]]) -> list[list[str]]:
    """
    This function finds all possible decryptions of a message, given a scrambled message and a key.
    The function first creates a list of possible decryptions for each pair of letters in the scrambled message.
    It then iterates through the list of possible decryptions, and for each possible decryption, it checks if it is a valid decryption.
    If it is, it adds the possible decryption to the list of possible decryptions.
    """
    message = decrypted[0]
    nospaces = [i for i in message if i != " "]
    key = decrypted[1]
    noSpacePossibles = findPossibles(nospaces,key,[])

    possibles = []
    for i in range(len(noSpacePossibles)):
        possibles.append([" " for i in message])
        index = 0
        for j in range(len(message)):
            if message[j] != " ":
                possibles[i][j] = noSpacePossibles[i][index]
                index += 1

    return (possibles)

def isWord(word:str) -> bool:
    return word.lower() in wordlist

def englishPossibles(possibles:list[list[str]]) -> list[str]:
    realPossibles = []
    for i in possibles:
        x = 0
        y = 0
        check = True
        for j in range(len(i)):
            if i[j] == " " or j == len(i):
                y = j
                if not isWord(''.join(i[x:y])):
                    check = False
                x = j+1
        if check:
            realPossibles.append(''.join(i))
    
    return (realPossibles)


if __name__ == "__main__":
    encrypted = encrypt("This message is encrypted")
    print(encrypted)
    decrypted = decrypt(encrypted)
    print(decrypted[0])
    possibles = givePossibles(decrypted)
    print(englishPossibles(possibles))
