from collections import Counter


five_letter_words = Counter()
# from http://www.kilgarriff.co.uk/bnc-readme.html
with open("./all.al", "r") as f:
    for line in f:
        try:
            freq, word, pos, numfiles = line.strip().split()
        except ValueError:  # oddness, like words with spaces in
            continue
        if len(word.strip()) == 5 and all(
            97 <= ord(char) <= 122 for char in word
        ):  # word is lowercase ascii
            five_letter_words[word] += int(freq)

g = open("five_letter_words.txt", "w")
for word, freq in five_letter_words.most_common():
    g.write(word)
    g.write(" ")
    g.write(str(freq))
    g.write("\n")3
g.close()