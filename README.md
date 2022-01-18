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

There are initially about 7900 candidate words. After the first guess, the candidate list is whittled 
to worst case about 600 words and (usually) exponentially down thereafter.

## Usage

The solver is written in Python 3, and has no external dependencies. Run:

```{bash}
./solver.py
```

It will suggest the best word (initially, OATER) and ask for the result. Type 5 characters to
indicate the result, such as `.y..Y` then press `ENTER`:

- ⬛ = `.`
- 🟨 = `y`
- 🟩 = `Y`

(If the suggested word isn't in the Wordle word list, type `n` and it will choose the next-best
word, but this is unlikely as the original word list is matched to the Wordle word list).

Once you type `YYYYY` the guesses will stop.

### Testing with a particular word

You can see what guesses the solver would use for a particular word, by using the `--test` parameter:
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

### Finishing what you have started

If you have started with your own guesses, you can provide these with `--guesses`, space-separated. You 
still need to provide the outcomes of the guesses, but the solver will pick up where you left off and 
find the next best word.

````
❯ ./solver.py --guesses laser bring crowd
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
Jolly good - that took 5 guesses
```

## Potential Improvements

- Where several words have the same or similar usefulness score, the guesser should return the most frequently-used one.
- We could probably exclude words that only occur once or twice in 100 million words, since they're unlikely to be chosen as 
answers (ZUPAN anyone?). BUT they might be good for discriminating.
- The solver always suggests words that match the information given (ie "hard mode"). Words that don't 100% match may 
be better for narrowing down large solution spaces, but exactly what the best discriminator is seems expensive to calculate.
````
