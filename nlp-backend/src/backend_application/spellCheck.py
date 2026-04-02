#******************************************************************************#
#* Name:     spellCheck.py                                                    *#
#* Author:   lvu                                                              *#
#*                                                                            *#
#* Description:                                                               *#
#*  Spell checking user entered input.                                        *#
#*                                                                            *#
#*                                                                            *#
#******************************************************************************#

import re
import os
import sys

from collections import Counter
# based on MIT https://github.com/jdlauret/SpellChecker/blob/master/spell_checker.py

from difflib import SequenceMatcher
def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def words(text): return re.findall(r'\w+', text.lower())

dir_path = os.path.dirname(os.path.realpath(__file__))
file_check_de = open('../data/SpellCheck/word_list_german_spell_checked.txt').read()
file_check_en = open('../data/SpellCheck/word_list_english_spell_checked.txt').read()

WORDS_de = Counter(words(file_check_de))
WORDS_en = Counter(words(file_check_en))


def P_de(word, N_de=sum(WORDS_de.values())):
    # "Probability of `word`."
    return WORDS_de[word] * 10 ** (len(word)) / N_de

def P_en(word, N_en=sum(WORDS_en.values())):
    # "Probability of `word`."
    return WORDS_en[word] * 10 ** (len(word)) / N_en

def correction(word):
    # "Most probable spelling correction for word."
    if word in file_check_de or word in file_check_en:
        return True, word
    else:
        return False, max(max(candidates(word), key=P_de),max(candidates(word), key=P_en))


def candidates(word):
    # "Generate possible spelling corrections for word."
        return (
            known_de([word])
            or known_de(similar_edit(word))
            or known_de(double_edit(word))
            or known_de(double_edit2(word))
            or known_de(double_back_edit(word))
            or known_de(double_back_edit2(word))
            or known_de(vowel_edit(word))
            or known_de(edits1(word))
            or known_de(edits2(word))
            or known_en([word])
            or known_en(similar_edit(word))
            or known_en(double_edit(word))
            or known_en(double_edit2(word))
            or known_en(double_back_edit(word))
            or known_en(double_back_edit2(word))
            or known_en(vowel_edit(word))
            or known_en(edits1(word))
            or known_en(edits2(word))
            or [word])

def known_de(words):
    # "The subset of `words` that appear in the dictionary of WORDS."
    return list(set(w for w in words if w in WORDS_de))
def known_en(words):
    # "The subset of `words` that appear in the dictionary of WORDS."
    return list(set(w for w in words if w in WORDS_en))

def vowels(char):
    # "Generate all possible vowels if the char is vowel, in other cases return empty list"
    vowels = 'aeiou'
    if char == 'a' or char == 'u' or char == 'i' or char == 'o' or char == 'e':
        return vowels
    else:
        return ''

def similar_to(char):
    # "Generates some similar characters if char satisfies any of conditions"
    if char == 'c':
        return 's'
    if char == 's':
        return 'c'
    if char == 'b':
        return 'p'
    if char == 'p':
        return 'b'
    if char == 'n':
        return 'm'
    if char == 'm':
        return 'n'
    if char == 'd':
        return 't'
    if char == 't':
        return 'd'
    else:
        return ''

def double_back_edit(word):
    # "Removing one of the 2 sequentially appearing characters in words (if there any)"
    splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deletes = [L + R[1:] for L, R in splits if len(R) > 1 if R[0] == R[1]]

    return set(deletes)

def double_back_edit2(word):
    # "Removing one of the 2 sequentially appearing characters in words (if there any) second time"
    deletes = []
    for e in double_back_edit(word):
        splits = [(e[:i], e[i:]) for i in range(len(e) + 1)]
        deletes = [L + R[1:] for L, R in splits if len(R) > 1 if R[0] == R[1]]

    return set(deletes)

def double_edit(word):
    # "Doing the same that the function above but on reverse direction (e.g. 'adres' -> 'address'"
    letters = 'bcdeflmnoprstvy'
    splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    inserts = [L + L[-1] + R for L, R in splits if L]

    return set(inserts)

def double_edit2(word):
    # "Same as double_back_edit2 but on reverse direction"
    letters = 'bcdeflmnoprstvy'
    for e in double_edit(word):
        splits = [(e[:i], e[i:]) for i in range(len(e) + 1)]
        inserts = [L + L[-1] + R for L, R in splits if L]

    return set(inserts)

def vowel_edit(word):
    # "Getting set of words where vowels are replaced(common mestake :) )"
    for e in double_edit(word):
        splits = [(e[:i], e[i:]) for i in range(len(e) + 1)]
        replaces = [L + c + R[1:] for L, R in splits if R for c in vowels(R[0])]

    return set(replaces)

def similar_edit(word):
    # "Getting set of where chars are replaced by similar ones (if any) (common mictake?)"
    for e in double_edit(word):
        splits = [(e[:i], e[i:]) for i in range(len(e) + 1)]
        replaces = [L + c + R[1:] for L, R in splits if R for c in similar_to(R[0])]

    return set(replaces)

def edits1(word):
    # "All edits that are one edit away from `word`."
    letters = 'abcdefghijklmnopqrstuvwxyz'
    splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deletes = [L + R[1:] for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]
    replaces = [L + c + R[1:] for L, R in splits if R for c in letters]
    inserts = [L + c + R for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)

def edits2(word):
    # "All edits that are two edits away from `word`."
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))

def edits3(word):
    # "All edits that are four edits away from 'word'."
    return (e3 for e2 in edits2(word) for e3 in edits2(e2))


# Assumes spell-testset1.txt and spell-testset2.txt are in the same dir.

def spelltestword(sentence):
    w=''
    inDic_counter = 0
    lastChar = sentence[-1]
    sentence = re.sub(r'[^\w\s]','',sentence)
    words = sentence.split(' ')
    for word in words:
        inDic,corrected = correction(word)
        if w == '':
            w = corrected
        else:
            w += " " + corrected
        if inDic:
            inDic_counter +=1
        ##print('{:.0%} of "{}" correct ({:.0%} unknown) '
        ##    .format(similar(corrected, word), word, (1-similar(corrected, word))))

    ##print('correction({}) => {:.0%} found in dictionay)'
    ##                .format(w, inDic_counter/len(words)))
    if lastChar == "?":
        w += "?"
    return w

    #Todos
    #add_word=''
    #print("Is this correct? y/n")
    #if input(add_word) == 'n':
    #    print('WORDS.valus().append(w)')
'''
def main():
    text=''
    print("Testlauf ...")
    print("Test 1 ...: siiemens")
    spelltestword('siiemens')
    print("Test 2 ...: wo befindett sich franhofer fokus und addidas")
    spelltestword('wo befindett sich franhofer fokus und addidas')
    print("Test 3 ...: ocherwises")
    print(spelltestword('ocherwises'))
    print("Testlauf Ende. Gebe etwas ein! Zum Beenden KeyboardInterrupt")


    while True:
        try:
            spelltestword(input(text))
        except KeyboardInterrupt:
            print("Interrupted by user")
            break
            sys.exit()

if __name__ == "__main__":
    main()
'''