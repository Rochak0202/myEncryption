kbAlphabet = "qwertyuiopasdfghjklzxcvbnm"
alphabet = "abcdefghijklmnopqrstuvwxyz"
numbers = "1234567890"

def scramble(phraseToScramble):
    encrypted = ""
    scrambleIndex = 0
    phraseToScramble = [i.lower() for i in phraseToScramble if i.lower() in (alphabet+" ")]
    scramblingPhrase = [i for i in phraseToScramble[::-1] if i != " "]

    for i in phraseToScramble:
        if i in alphabet:
            encrypted += kbAlphabet[(kbAlphabet.index(i)+alphabet.index(scramblingPhrase[scrambleIndex])+1)%26]
            scrambleIndex += 1
        else:
            encrypted += i

    return encrypted

pairMatches = {i+j:[] for i in alphabet for j in alphabet}
for i in alphabet:
    for j in alphabet:
        pairMatches[scramble(i+j)].append(i+j)

def unscramble(encrypted):
    decrypted = [" " for i in encrypted]
    nospaces = [i for i in encrypted if i != " "]
    decryptedletters = ["" for i in nospaces]
    unsureCount = 1
    unsureList = []
    half = int(len(nospaces)/2)
    if len(nospaces)%2 == 1:
        half+=1

    for i in range(half):
        pair = nospaces[i]+nospaces[-i-1]
        if len(pairMatches[pair]) == 1:
            decryptedletters[i] = pairMatches[pair][0][0]
            decryptedletters[-i-1] = pairMatches[pair][0][1]
        elif len(pairMatches[pair]) > 1:
            decryptedletters[i] = str(unsureCount)
            decryptedletters[-i-1] = str(unsureCount)
            unsureList.append((unsureCount, pairMatches[pair]))
            unsureCount+=1
            unsureCount = unsureCount%10

    j = 0
    for i in range(len(decrypted)):
        if encrypted[i] != " ":
            decrypted[i] = decryptedletters[j]
            j += 1


    decrypted = ''.join(decrypted)
    return (decrypted, unsureList)

def findPossibles(nospaces, key, possibles):
    possible = [i for i in nospaces]
    half = int(len(nospaces)/2)
    if len(nospaces)%2 == 1:
        half+=1

    for i in range(half):
        if nospaces[i] in numbers:
            for j in key[0][1]:
                possible[i] = j[0]
                possible[-i-1] = j[1]
                if len(key) == 1:
                    possibles.append([i for i in possible])
                else:
                    findPossibles(possible, key[1:], possibles)
    
    return possibles


def givePossibles(decrypted):
    message = decrypted[0]
    nospaces = [i for i in message if i != " "]
    key = decrypted[1]
    possibles = findPossibles(nospaces,key,[])

    format = [" " for i in message]
    for i in possibles:
        index = 0
        for j in range(len(message)):
            if message[j] != " ":
                format[j] = i[index]
                index += 1
        print (''.join(format))


if __name__ == "__main__":
    encrypted = scramble("Hello World")
    decrypted = unscramble(encrypted)
    print(encrypted)
    print(decrypted[0])
    print(decrypted[1])
    givePossibles(decrypted)