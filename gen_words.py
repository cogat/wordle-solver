from collections import Counter
from wordle_wordlist import La, Ta

WORDLE_WORDS = set(La + Ta)

five_letter_words = Counter()
# from http://www.kilgarriff.co.uk/bnc-readme.html
with open("./all.al", "r") as f:
    for line in f:
        try:
            freq, word, pos, numfiles = line.strip().split()
        except ValueError:  # oddness, like words with spaces in
            continue
        if (
            len(word.strip()) == 5 and word.lower() in WORDLE_WORDS
        ):  # word is lowercase ascii
            five_letter_words[word] += int(freq)

g = open("five_letter_words.txt", "w")
for word, freq in five_letter_words.most_common():
    g.write(word)
    g.write(" ")
    g.write(str(freq))
    g.write("\n")
g.close()