from collections import Counter, defaultdict
import re

MOCK_ANSWER = "TROLL".upper()

print("Loading word freqs")
words = Counter()
f = open("five_letter_words.txt", "r")
for line in f:
    word, freq = line.split()
    words[word] = int(freq)
f.close()
del words["erato"]  # top 1st guess, but not in Wordle's list


def mock_wordle(*, guess, answer):
    """
    A Wordle simulator for testing with
    """
    assert len(guess) == len(answer)
    result = ""
    for g, a in zip(guess.upper(), answer.upper()):
        if g == a:
            result += "Y"
        elif g in answer.upper():
            result += "y"
        else:
            result += "."
    assert len(result) == len(answer)
    return result


ALPHABET = "abcdefghijklmnopqrstuvwxyz"
ALPHABET_SET = set(ALPHABET)


class WordleSolver:
    candidate_words: Counter
    filter_components: list  # stores sets of allowed letters for each position
    must_have_letters: set
    num_guesses = 0

    def __init__(self, *, words):
        self.candidate_words = words
        self.must_have_letters = set()
        self.filter_components = [ALPHABET_SET.copy() for _ in range(5)]

    def get_best_word(self):
        """
        Return the word most likely to be the answer.

        Factors:
        - the most likely letters appear in the most candidate words, adjusted for word frequency.
        - the most likely words contain the greatest sum of letter likelinesses.

        TODO:
        We don't always want the most likely answer. Sometimes we might want to get the word that
        best discriminates the remaining candidate words.

        In some circumstances (e.g. perhaps "zelle", which has an inefficient naive guess path)
        a non-candidate word might even be a better discriminator. If we're in a situation where
        we know many letters but there are still relatively many candidate words, perhaps a
        non-candidate guess will yield more information.
        """
        # print("Arranging letters according to net frequency")
        total_wordfreqs = Counter()
        for word, word_frequency in self.candidate_words.items():
            for letter in set(word):  # ignore repeated letters
                total_wordfreqs[letter] += word_frequency

        # print("Arranging words by letter usefulness")
        word_usefulness = Counter()
        for word in self.candidate_words:
            for letter in set(word):
                word_usefulness[word] += total_wordfreqs[letter]

        return word_usefulness.most_common()[0][0]

    def filter_words(self):
        """
        Use what is known about letters to reduce the candidate word set.
        """
        pattern = r"^"
        for fc in self.filter_components:
            letters = "".join(sorted(list(fc)))
            pattern += rf"[{letters}]"
        pattern += r"$"
        regex = re.compile(pattern)

        new_words = Counter(
            {
                w: f
                for w, f in self.candidate_words.items()
                if regex.match(w)
                and self.must_have_letters & set(w) == self.must_have_letters
            }
        )
        if len(new_words) == 0:
            import pdb

            pdb.set_trace()
            raise Exception("No candidate words left, sorry", pattern)
        self.candidate_words = new_words
        print(f"Filtered down to {len(self.candidate_words)} words, {pattern[1:-1]}")

    def apply_guess(self, *, guess: str, result: str):
        """
        Update what is known about letters from the guess.
        """
        if result in ("n", "N"):
            del self.candidate_words[guess]
            return

        self.num_guesses += 1
        for i, (g, r) in enumerate(zip(guess, result)):
            if r == ".":  # the letter is not here
                self.filter_components = [fc - {g} for fc in self.filter_components]
            elif r == "y":  # the letter must be somewhere, but not here
                self.must_have_letters.add(g)
                self.filter_components[i] -= {g}
            elif r == "Y":  # the letter is here
                self.must_have_letters.add(g)
                self.filter_components[i] = {g}

        self.filter_words()


def guess_loop(mock_answer=MOCK_ANSWER):
    solver = WordleSolver(words=words.copy())
    if not mock_answer:
        print(
            """
        Outcome is:
            n (whole answer) = not in word list
        or 5 letters:
            . = not in letters
            y = in letters but not in place
            Y = in letters and in place
        e.g. YYYYY = perfect"
        """
        )
    while True:
        guess = solver.get_best_word()
        print(f"Suggest '{guess.upper()}'")
        if mock_answer:
            result = mock_wordle(guess=guess, answer=mock_answer)
            print(f"outcome: {result}")
        else:
            result = input("Outcome? ")

        if result == "YYYYY":
            # +1 becuase the correct guess isn't applied to the solver
            print(f"Jolly good - that took {solver.num_guesses + 1} guesses")
            return solver.num_guesses + 1
        else:
            solver.apply_guess(guess=guess, result=result)


def find_hardest_word():
    hardest_num_guesses = 0
    results = []
    for word in list(reversed(words)):
        print(f"Trying with {word.upper()}")
        num_guesses = guess_loop(mock_answer=word)
        hardest_num_guesses = max(num_guesses, hardest_num_guesses)
        if num_guesses == 6:
            results.append((word, num_guesses))
            if len(results) == 10:
                return results
    return results


if __name__ == "__main__":
    # guess_loop(mock_answer="zupan")
    guess_loop(mock_answer=None)
    # print(find_hardest_word())