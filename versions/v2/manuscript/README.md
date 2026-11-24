# A signed-weight extension of Frid's recurrence for the Thue–Morse prefix problems of Ambrož, Kadlec, Masáková and Pelantová

**Authors:** Haobo Ma (ChronoAI Pte Ltd, Singapore); Wenlin Zhang (National University of Singapore; ChronoAI Pte Ltd, Singapore).

**License:** Creative Commons Attribution 4.0 International, `cc-by-4.0`.

## Results and attribution

For the zero-start Thue–Morse prefix of length `n`, combined pal-antipal length `C(n)` equals minimum signed binary weight `W(n)`. Ordinary palindromic length satisfies `C(n)<=P(n)<=2C(n)`, with both endpoints at every positive mixed cost.

For every `k>=1`, the first prefix with `C(n)=k`, also the first with `P(n)=C(n)=k`, has length `(2*4^(k-1)+1)/3`. This proves all first occurrences in Table 2 of the posing source. Consequently `limsup C(n)/ln(n)=1/ln(4)` and `liminf C(n)/ln(n)=0`. The nonempty palindromic prefixes have exactly lengths `4^r`; antipalindromic prefixes exactly lengths `2*4^r`, for `r>=0`.

The shifted factor `t[1:7)=110100` has ordinary cost three and mixed cost one. The arbitrary-factor extension was not asserted in the source. The note establishes attainment at the factor-two endpoint for every mixed cost, but not a general first-occurrence formula for that endpoint.

Frid's ordinary-length recurrence is prior work, first posted on 22 June 2019. Li's later independent ordinary-length work, first posted on 29 July 2019, acknowledges Frid. The signed-weight arithmetic and its record positions are classical: OEIS A007302 and A007583. The mixed-prefix interpretation is the subject of this note. Further attribution and exact locators are in `note.tex`.

## Build

Extract `source-v2.zip` and run:

```sh
tectonic note.tex
```

Use Tectonic 0.17.0, or standard LaTeX:

```sh
pdflatex -interaction=nonstopmode -halt-on-error note.tex
pdflatex -interaction=nonstopmode -halt-on-error note.tex
```

The bibliography is contained in `note.tex`; no external bibliography file or BibTeX pass is required. Standard packages are `geometry`, `fontenc`, `lmodern`, `amsmath`, `amssymb`, `amsthm`, `booktabs`, `array`, `longtable`, and `hyperref`.

## Exact finite checks

Python 3.10 or later and its standard library suffice:

```sh
python3 verify.py --bound 8192 --output verification.json
```

The checker computes actual ordinary and mixed minima on every prefix through length 8192, checks each allowed cut, and compares the minima with signed weights and Frid's recurrence. Direct slicing independently checks the factor predicates and complete prefix-type classification through length 128. First equal-cost occurrences in the word window are compared with the all-cost formula. Displayed source-table values beyond that window are recurrence evaluations, not materialized long-word minima. The affine identities and classical formula `W(n)=popcount(n XOR 3n)` are checked for `0<=n<=100000`; the shifted-factor example is checked directly. Expected output has `status: pass`; `verification.json` gives the exact ranges, counts and digest. All arithmetic is integral. Universal results have the written proofs in `note.tex`.

## Formal scope

The following links select scientific revision `106c79bbb6571a3dc7c60f4b2146860d56e88fc5`:

- [ThueMorseSignedCut.lean](https://github.com/the-omega-institute/trureturing/blob/106c79bbb6571a3dc7c60f4b2146860d56e88fc5/D5/S1/Words/Palindromes/ThueMorseSignedCut.lean): `MixedFactors` and `combinedLength` specify consecutive nonempty allowed factors and their minimum; `allowed_factor_signed_cut` gives `W(j)<=W(i)+1` on an allowed factor; `combined_prefix_signed_lower` gives `W(n)<=C(n)<=P(n)`.
- [ThueMorseSharpPrefix.lean](https://github.com/the-omega-institute/trureturing/blob/106c79bbb6571a3dc7c60f4b2146860d56e88fc5/D5/S1/Words/Palindromes/ThueMorseSharpPrefix.lean): `prefix_signed_upper` gives `P(n)<=2W(n)`; `sharp_factor_two_prefix` gives the universal comparison and a positive attaining prefix.
- [ThueMorseAttainment.lean](https://github.com/the-omega-institute/trureturing/blob/106c79bbb6571a3dc7c60f4b2146860d56e88fc5/D5/S1/Words/Palindromes/ThueMorseAttainment.lean): `family_attains` gives `W(a_r)=C(a_r)=P(a_r)=r+1`, where `a_0=1`, `a_(r+1)=4a_r-1`; `unbounded_equal_cost` gives `C=P>=K` on a positive prefix for each `K>=1`.

The equality `C=W`, first-occurrence and growth formulas, complete prefix-type classification, affine sharp family and shifted-factor example have written proofs beyond these selected declarations' scope.

## Posing source

P. Ambrož, O. Kadlec, Z. Masáková and E. Pelantová, *Palindromic length of words and morphisms in class P*, Theoretical Computer Science 780 (2019), 74–83, DOI `10.1016/j.tcs.2019.02.024`. Locators refer to arXiv:1812.00711v2, Section 6, printed p.13, final paragraph; Tables 1–2, p.14. The coverage table treats their source assertions separately from general questions and unposed extensions.
