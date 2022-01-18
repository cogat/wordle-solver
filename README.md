# Wordle Solver

This solver uses a list of 5-letter words plus usage frequency (occurrences per 100 million words -
of all lengths - in the source text), derived from
[this source](http://www.kilgarriff.co.uk/bnc-readme.html) to resource guesses that preference more
common words.

## How it works

Basically:

1. Find all the words that match the information so far (the candidate words).
2. For each candidate word, add the word's usage frequency to a tally for each letter. Then we will
   know the overall most frequently-used letters.
3. For each candidate word, add the precalculated value of its letters to get the value of the
   word.
4. Use the most valuable word as the next guess.
5. Repeat until done.

There are initially about 30,500 candidate words (not all of these are in the Wordle list but they
can be skipped if so). After the first guess, the candidate list is whittled to maximum of 2000
words.

## Usage

Run:

```{bash}
python3 solver.py
```

It will suggest the best word (initially, OATER) and ask for the result. Type 5 characters to
indicate the result, such as `.y..Y` then press `ENTER`:

- ⬛ = `.`
- 🟨 = `y`
- 🟩 = `Y`

If the suggested word isn't in the Wordle word list, type `n` and it will choose the next-best
word. Once you type `YYYYY` the guesses will stop.

```
❯ ./solver.py --test=favor
Suggest 'OATER'
Outcome? yY..Y
Filtered down to 9 words, [abcdfghijklmnpqrsuvwxyz][a][abcdfghijklmnopqrsuvwxyz][abcdfghijklmnopqrsuvwxyz][r]
Suggest 'MAJOR'
Outcome? .Y.YY
Filtered down to 6 words, [abcdfghiklnpqrsuvwxyz][a][abcdfghiklnopqrsuvwxyz][o][r]
Suggest 'RAZOR'
Outcome? .Y.YY
Filtered down to 5 words, [abcdfghiklnpqsuvwxy][a][abcdfghiklnopqrsuvwxy][o][r]
Suggest 'LABOR'
Outcome? .Y.YY
Filtered down to 3 words, [acdfghiknpqsuvwxy][a][acdfghiknopqrsuvwxy][o][r]
Suggest 'FAVOR'
Outcome? YYYYY
Jolly good - that took 5 guesses
```

If you have started with your own guesses, you can provide these with `--guesses`. You still need
to provide the outcomes of the guesses, but the solver will pick up where you left off and find the
next best word.

````
❯ ./solver.py --guesses laser bring crowd

        Outcome is:
            n (whole answer) = not in word list
        or 5 letters:
            . = not in letters
            y = in letters but not in place
            Y = in letters and in place
        e.g. YYYYY = perfect"

Suggest 'LASER'
Outcome? ....y
Filtered down to 251 words, [bcdfghijkmnopqrtuvwxyz][bcdfghijkmnopqrtuvwxyz][bcdfghijkmnopqrtuvwxyz][bcdfghijkmnopqrtuvwxyz][bcdfghijkmnopqtuvwxyz]
Suggest 'BRING'
Outcome? .Y...
Filtered down to 32 words, [cdfhjkmopqrtuvwxyz][r][cdfhjkmopqrtuvwxyz][cdfhjkmopqrtuvwxyz][cdfhjkmopqtuvwxyz]
Suggest 'CROWD'
Outcome? .YY..
Filtered down to 10 words, [fhjkmopqrtuvxyz][r][o][fhjkmopqrtuvxyz][fhjkmopqtuvxyz]
Suggest 'PROOF'
Outcome? YYY..
Filtered down to 3 words, [p][r][o][hjkmpqrtuvxyz][hjkmopqtuvxyz]
Suggest 'PROXY'
Outcome? YYYYY
Jolly good - that took 5 guesses```

## Potential Improvements

- Where several words have the same or similar usefulness score, the guesser should return the most frequently-used one.
- We could probably exclude words that only occur once or twice in 100 million words, since they're unlikely to be chosen as answers. BUT they might be good for discriminating.
- The solver always suggests words that match the information given (ie "hard mode"). Words that don't 100% match may be better for narrowing down large solution spaces, but exactly what the best discriminator is seems expensive to calculate.
````
