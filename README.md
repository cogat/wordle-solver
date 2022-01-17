# Wordle Solver

This solver uses a list of words plus usage frequency, derived from [this source](http://www.kilgarriff.co.uk/bnc-readme.html) to resource guesses.

## How it works

Basically:

1. Find all the words that match the information so far (the candidate words).
2. For each candidate word, add the word's usage frequency to a tally for each letter. Then we will know the overall most frequently-used letters.
3. For each candidate word, add the precalculated value of its letters to get the value of the word.
4. Use the most valuable word as the next guess.
5. Repeat until done.

There are initially about 30,500 candidate words (not all of these are in the Wordle list but they can be skipped if so). After the first guess, the candidate list is whittled to maximum of 2000 words.

## Usage

Run:
```{bash}
python solver.py
```

It will suggest the best word (initially, OATER) and ask for the result. Type 5 characters to indicate the result, such as `.y..Y` then press `ENTER`:

* ⬛ = `.`
* 🟨 = `y`
* 🟩 = `Y`

If the suggested word isn't in the Wordle word list, type `n` and it will choose the next-best word. Once you type `YYYYY` the guesses will stop.
