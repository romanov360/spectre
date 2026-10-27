# Code review: `paper-prepub-review-squashed` (c10575c)

Adversarial review of the code: the Python generators, ledgers, checkers, certificates and tests. It covers the one
commit on top of brentharts/spectre master and gives extra weight to the files that commit changes. The commit
message, `PREPUB_FIXES.md` and the READMEs were treated as claims to verify. No paper source was edited, and the Lean
build and the 4D search were not rerun.

Every finding below was verified, either by running code (the commands are given) or by tracing a concrete path
through it. Anything uncertain is marked as such. Line numbers refer to c10575c.

## Summary

| # | Severity | Where | One line |
|---|---|---|---|
| 1 | **Major** | `spectrepaper.py:287`, `spectre_golden.py:212` | "52 edge types, 34 obey the recurrence" counts 12 types that never occur in the stated range 1 ≤ k ≤ 6; their all-zero sequences pass vacuously |
| 2 | Minor | `spectrepaper.py:2685`, `chair44facts.py:375`, `hierarchy_certificate/chair44_blocks_indep.py` | the 360,189 / 15,214 "reproduction" is not checked by any code: the selftest compares a hard-coded constant with itself, and the independent script asserts nothing |
| 3 | Minor | `spectre_boundary.py:493`, `spectrepaper.py` (prop:sstar) | the exact interface law is claimed at depths 4 and 5 but tested only at 3 and 4; the fitted values 2.66/2.41 are hard-coded and unchecked |
| 4 | Minor | `spectrefacts.py:1530`, `boundary_certificate/check_spectre_boundary_proof.py:309` | `boundary_exact` says the ledger sequence agrees with an exact recount, but no code compares the two; the claim still says Q(√3) while the method now says Z[ζ₁₂] |
| 5 | Minor | `chair44_lines.py:116`, `chair44facts.py:414,515` | the new exact line lengths 2ⁿ / 2ⁿ−1 ("checked at depth 5") are checked nowhere; the ledger still records and asserts the old length 2⁶−2 = 62 |
| 6 | Minor | `lean_rebuild/discharge_audit_indep.py` | the "independent" audit transliterates the upstream algorithm, blind spots included; its statement parser and `sorry` scan are weaker than described |
| 7 | Minor | `spectre_supplement.py:142-157`, `spectrepaper.py:2607-2609`, `monotilefacts.py:224` | several selftest checks cannot fail: tautologies, and an `and … or` precedence slip |
| 8 | Nit | `boundary_certificate/spectre_window.py:280` | "all four window types are reached" is printed but not asserted |
| 9 | Nit | `nd_search/chair_nd_fast.py:140-160`, `nd_search/anneal4d.py` | the objective changes units on one `cap` path, Σ counts above the cap are truncated, and a restart's starting state is never a candidate for "best"; none of this affects the reported 273 |
| 10 | Nit | `hierarchy_certificate/chair44_blocks_indep.py:262` | the (0,0,2) address test accepts either digit order, so it cannot fail on an ordering mistake |

---

## Findings

### 1. Major: the fine boundary decomposition counts 12 types that are absent from the stated range

**Where:** `spectrepaper.py:287-292` (text: "Resolved by species and edge index, the boundary has $52$ edge types, and
counted on placed tiles for $1\le k\le6$ (… the single tile at $k=0$ is dropped) only $34$ of them satisfy the
recurrence"). The conclusion repeats it, and the commit message lists it as a fix ("52 edge types: 34 obey the
recurrence, 14 are bounded"). The numbers come from `spectre_golden.component_audit` (`spectre_golden.py:212-234`) and
are hard-coded in the text. No selftest compares them.

**What is wrong:** `component_audit` takes `types` from the union over **all** orders, k = 0 included
(`set().union(*[set(c) for c in comps])`). It then drops k = 0 from each sequence (`drop=1`). Twelve Δ edge types
occur only at k = 0, the single tile. Over 1 ≤ k ≤ 6 their sequences are `[0,0,0,0,0,0]`, which satisfy
`s[i] == 5 s[i-1] - 3 s[i-2] - s[i-3]` vacuously. On the range the paper names, then, there are 40 edge types, not 52, and
22 of them obey the recurrence, not 34. The 14 period-two and 4 growing types are correct. So is the Ψ sequence
0, 5, 31, 141, 607, 2581.

**Reproduction:**
```
python3 - <<'EOF'
import spectre_golden as G
comps = G.boundary_components(6)
types, obey, fail, p2 = G.component_audit(comps)
print(len(types), len(obey), len(fail), len(p2))                     # 52 34 18 14
print([t for t in types if all(comps[k].get(t,0)==0 for k in range(1,7))])
# [('Delta',0),('Delta',1),('Delta',2),('Delta',3),('Delta',4),('Delta',7), …, ('Delta',13)]  -> 12 types
print(sum(1 for t,s in obey if not any(s)))                           # 12 obeying sequences are all zero
EOF
```

**Why it matters:** the paragraph exists to support the conclusion's claim about how much of the fine boundary
the recurrence governs. The reported share, 34/52 = 65%, is inflated by vacuous passes. The true share is
22/40 = 55%.

**Fix:** in `component_audit`, build `types` from `comps[drop:]`, or skip all-zero sequences. Have the text read
"40 edge types … 22 of them" (or state the 12 vacuous ones explicitly). Generate these counts from the code, not by
hand, and add a selftest check.

### 2. Minor: the admissible-block "reproduction" is not checked by any code

**Where:**
- `chair44facts.py:375` records `romanov=dict(legal=1410, fixed_seeds=27, admissible=360189, admissible_recomputed=False)`, a literal.
- `spectrepaper.py:801` fills `@adm@` in "reproduces @adm@ admissible blocks" from that literal.
- `spectrepaper.py:2685` checks `hu['romanov']['admissible'] == 360189`, which compares the literal with itself.
- `hierarchy_certificate/chair44_blocks_indep.py` has **no** assertion on any of its headline numbers (2388/1194/44, 30,
  1410, 27, 360,189, 15,214, 0). It prints them. Nothing reads `out_chair44_blocks_indep.txt`.

**What is wrong:** the paper says the new implementation "reproduces" these counts. The only evidence is a text file
compared by eye. If the script printed 360,188 next time, nothing would fail. The 15,214 orbit count is not even a
ledger value; it is typed into the text twice (`spectrepaper.py`, `chair44facts.py:384`).

**Reproduction:** `grep -n "assert" hierarchy_certificate/chair44_blocks_indep.py` shows only structural asserts
(input sizes, tiling, no border contacts). None of them is on a result. The re-run (see "What I checked") matches the
committed output exactly, so the numbers themselves are right.

**Fix:** put `assert len(RAW)==2388`, `len(LEGAL)==44`, `len(P0)==30`, `counts==[…,1410,1410]`,
`len(admissible)==360189`, `len(orbits)==15214` and `bad==0` at the end of the script. Alternatively, have a slow test
parse the output file and compare it with the ledger, and make the ledger hold 15,214 too.

### 3. Minor: the exact interface law is tested at depths 3 and 4, but the paper claims depths 4 and 5

**Where:** `spectre_boundary.py:493-497`. The selftest loops `for N in (3, 4)`. The paper (prop:sstar and the paragraph
after it) says the closed form "matches those counts exactly at both depths", meaning 4 and 5. It quotes the fitted
growth 2.66 and 2.41 as hard-coded text. `spectrepaper --selftest` checks only that the string `N_{\Gamma}(c)Q(N-c)`
is present (`spectrepaper.py`, check "the interface count carries the Mystic perimeter"); it does not run
`spectre_boundary`. The commit message's "the selftest checks it" is true only of `spectre_boundary.py --selftest`, and
only at depths 3 and 4.

**Verification (the claims are correct):**
```
N=5: measured [5794, 16686, 37676, 82552, 220156] == predicted, exactly
fits: depth 4  measured 2.6575, closed form 2.6575, without Mystic 2.6163
      depth 5  measured 2.4071, closed form 2.4071, without Mystic 2.3817
```
(by calling `measured_interfaces`, `predicted_interfaces` and `naive_fit` for N = 3, 4, 5).

**Fix:** add N = 5 to the selftest loop (it costs about a minute), and generate 2.66/2.41 (and 2.62/2.38 in the
module docstring) from `naive_fit` rather than typing them.

### 4. Minor: `boundary_exact` cites a comparison that no code makes

**Where:** `spectrefacts.py:1530-1538` (the commit changes the method text); `boundary_certificate/check_spectre_boundary_proof.py:300-312`.

**What is wrong:**
- The fact's `value` is `BOUNDARY_SEQ`, which is `boundary_perimeter(6)`: the recurrence run from the hard-coded seed
  `(14, 46, 182)` (`spectrefacts.py:1374-1387`). It is not a count.
- The method says the sequence is "recounted … in an independent implementation (boundary_certificate/spectre_exact.py,
  'matches the exact patches for k = 0..6')". That assertion in the certificate compares the exact patch counts with the
  certificate's **own** `PO` (from its 95×95 matrix), not with `spectrefacts.BOUNDARY_SEQ`. The certificate imports
  nothing from the repository, by design.
- The pyCICY cross-check that does compare with `BOUNDARY_SEQ` returns `None` (silently skipped) when pyCICY is absent,
  as it is here.

So the agreement "ledger sequence = exact count" is established by a person reading two printouts. (They do agree:
`[14, 46, 182, 758, 3198, 13534, 57318]` in both.) The fact's `claim` also still reads "counted exactly in
$\mathbb{Q}(\sqrt3)$", while the new method says "exact coordinates in Z[zeta_12]".

**Fix:** add a ledger test that runs `spectre_exact`'s level builder (or reads `out_spectre_boundary_proof.txt`) and
asserts equality with `BOUNDARY_SEQ`, and align the claim text with the method.

### 5. Minor: the new exact stack-line lengths are not checked, and the ledger still asserts the old one

**Where:** `chair44_lines.py:116-141`, `chair44facts.py:414` and `:515`, and the paper text
("of length $2^{n}$ on the main diagonal and $2^{n}-1$ for the other six cells").

**What is wrong:** the commit changes the paper from 2ⁿ−2 to the exact lengths and says "Checked at depth 5". In fact:
- `stack_check` still tests only `range(N - 2)` from each corner offset. It still returns `length=N-2`, and only its
  docstring was edited.
- The ledger `chair_lines` stores `stack_length=lr['stack'][0]['length']` (= 62), and its selftest asserts
  `ln['stack_length'] == 62`.
- No code checks 64 or 63.

The paper's claim does follow from `tube_invariance` together with the counting formula given in the text. A direct
check at depth 5 confirms it: for each of the six stack labels, the lines with difference e ∈ T have 32, 31, 31, 31,
31, 31, 31 cells, each with a single label. Still, the number the ledger records contradicts the number the paper
states.

**Fix:** make `stack_check` scan the full intersection of each line with the cube, record the lengths per
difference, and assert `{(0,0): 2**n, others: 2**n - 1}` in `run_tests` and in the ledger.

### 6. Minor: `discharge_audit_indep.py` is not independent in method, and its extra checks are weaker than described

**Where:** `lean_rebuild/discharge_audit_indep.py`; the README and paper ("written independently of the project's own
audit").

**What is wrong:**
1. **Same algorithm.** I fetched upstream `lean/R44/scripts/discharge_diff_audit.sh` at `d53d224` into an isolated
   directory and read it. The "independent" script has the same structure throughout: the same `difflib.SequenceMatcher`
   opcodes, the same rule that one marker anywhere in a replace/insert hunk accepts the whole hunk, the same
   `block_coverage` state machine, and the same deletion-bracketing test. That is a transliteration. Any blind spot of the
   upstream rule is shared. For example, one `-- [compile-fix]` marker on a single line accepts an arbitrarily large
   contiguous hunk; `CarrierCoordinateStates.lean` has 753 changed lines.
2. **Statement comparison.** This is the genuinely new part, but it is coarser than the README says:
   - `statements()` cuts each statement at the first `:=` or `where`, so a `:=` inside a binder or a `let` truncates it;
   - it reads at most 60 lines;
   - it keys declarations by bare name, so two declarations with the same name in different namespaces overwrite each
     other;
   - it strips only `--` comments, not `/- … -/` blocks.
3. **`sorry` scan.** Because block comments are not stripped, the scan lists 9 "risky" lines. Two are prose in
   docstrings (`ConcreteCompanions.lean:7`, `RegisteredComponentGeometry.lean:11`). The README's "seven changed lines …
   `native_decide`" is the right count, but it was reached by hand, not by the script.
4. **The classification is not computed.** "All 76 declaration diffs are notation or listed benign changes" is a
   human classification. The script prints the diffs and asserts only `npass == len(files)`.

**Verified sound:** the file → delivery-archive assignment for all 67 files is identical to upstream's explicit
per-exchange lists, though it is derived differently ("newest archive containing the file"). The script
`map.py` compares the two.

**Fix:** describe the script as a re-implementation of the same rule plus a statement diff, not as an independent audit.
Strip block comments before the `RISKY` scan. Key statements by `(namespace, name)`. Compare full declaration headers
up to the `:=` at bracket depth 0.

### 7. Minor: selftest checks that cannot fail

- `spectre_supplement.py:142-149`: "the quoted Fact count is the real one" checks `'all %d' % len(P.paper_facts())`
  against a document whose number was produced by the same expression (`preface()`, `:60-63`). "the quoted count of
  numbered Facts" does the same with `P.document().count(r'\begin{fact}')`. These checks can fail only if the template
  wording changes, never if a count is wrong. The preface's "%d theorems, kernel-accepted, no admitted proofs" counts
  theorem *names* in the generated Lean text (`L.theorem_names(L.document())`). That is not evidence of kernel acceptance.
- `spectrepaper.py:2607-2609` (pre-existing): `A and B and C and D or str(support) in text` parses as `(…) or (…)`.
  Because "93" appears elsewhere in the paper ("close on $93$ types"), the check passes with every rank wrong:
  ```
  ct={'spectre':{'rank':13},'chair':{'rank':0,'bipartite':True,'support':93}}
  -> check passes with wrong ranks: True ; with support=1: True
  ```
  The ranks are asserted separately in `monotilefacts.selftest`, so nothing is actually unverified. The check is
  vacuous all the same. Fix: add parentheses, and drop the `or` fallback.
- `monotilefacts.py:224` and `chair44facts.py:543` (pre-existing): `all(key in KIND for key in KIND)` is always true.

### 8. Nit: `spectre_window.py` does not assert the result the README claims

`boundary_certificate/spectre_window.py:280-283` computes `wt`, the window types reached by the lower-bound block, and
only prints it. The README and Theorem 3 rely on "All four are reached". It holds: the output lists `('G',0), ('G',1),
('O',0), ('O',1)`, and my re-run matches. Add `assert len(wt) == 4`. Similarly, `check_spectre_fractal.py` asserts
`('O','O') in sib_shapes`, which is good; the window script should do the same.

### 9. Nit: rough edges in the 4D annealing objective (they do not affect the reported numbers)

`nd_search/chair_nd_fast.py`, `Fast.closure`:
- The second `cap` exit, `if len(newP) > cap: return ('cap', len(newP), sizes)`, omits `s0` even when
  `want_sigma0=True`. `anneal4d.score` then falls back to `r[1] = |P|`, a different quantity from |Σ(P₀)|.
- `Sigma()` stops after the batch in which `len(out) > cap`, so any Σ size above the cap is a batch-dependent lower
  bound.

Neither affects 273: a value ≤ 2500 on the first path is exact, and the second path needs |P| > 2500. Also,
`anneal4d.py` updates `best` only on accepted moves, so the starting state of each restart (including the canonical
start of seed 21) is never a candidate. Offset states score 2|P|, which can be lower than the closable states' Σ values,
so the walk is biased toward dead ends. The README already notes that offset scores are even. The sum
2399 + 3208 + 3424 + 3101 = 12,132 and the seed-11 best of 273 both match the logs. So do 4288 + 4212 + 4284 = 12,784,
with half F and half R, all at the cap.

### 10. Nit: the coincidence-address test in `chair44_blocks_indep.py` accepts either digit order

Line ~262 prints `(0,0,2) among them` for most-significant-first addresses and also `any(...)` for the reversed order.
Both are `True` in the output, so the line cannot detect an ordering mismatch with the paper's convention. Assert the
one ordering the paper uses.

---

## What I checked and found sound

Runs (all on this branch, clean tree):
- `python3 spectre_supplement.py --selftest`: all checks pass (about 3 minutes, not "fast").
- `timeout 1500 python3 spectrepaper.py --selftest`: `120022 characters, 12 sections, all checks pass`, exit 0. No
  check is skipped. Most of its checks are string-presence checks on the generated text; the recomputing ones
  (`MFT.selftest`, `HU.run_tests`, `LN.run_tests`, `CU/CSL/FD`) all ran.
- `python3 spectre_boundary.py --selftest`: all pass. I also checked the interface identity at depth 5 by hand (see #3).
- `chair44_lines.run_tests()`: ok. The new d_z corner-line tests pass and test what the text says: sums in {0,1,2} on
  (0,0,1), sums = L on (1,0,0), and τ sends the closed class onto two words.
- `chair44_twist.verify()`: ok. The frame counts at depths 1, 2, 3 are 7, 24, 24, so "depth 2" is correct.
- `chair44facts` coincidence counts `[1, 8, 64, 176, 400, 848, 1744, 3536, 7120]` satisfy c(M) = 28·2ᴹ − 48 from M = 1,
  so the extended range is right.
- `boundary_certificate/spectre_window.py` re-run: identical to `out_spectre_window.txt` (1192 live types; separation
  1.909; nearest identity-type distance 4.114; x⁴−10x²+1; all four window types). The "at most 1193 pieces" argument
  traces correctly:
  - two pieces meeting a small disc are within the pruning radius, so their type and their ancestors' types are live;
  - `sep > 1` makes the type → relative placement map injective within a class;
  - the identity check rules out two addresses giving the same map.
- `boundary_certificate/check_spectre_fractal.py` re-run: see the note at the end of this file.
- The fine-decomposition sequences in the text (Π: 1, 7, 22, 91, 378, 1599; Ψ: 0, 5, 31, 141, 607, 2581; 14 period-2
  types) and the failure of the order-4 extension (x²−1)(x²−4x−1) on Π (379 ≠ 378) are reproduced. Only the 52/34 totals
  are wrong (#1).
- `predicted_interfaces` index ranges: `Q = mystic_perimeter(depth-1)` is indexed at `depth-c` ≤ `depth-1`, so there is
  no off-by-one, and equality is exact at N = 3, 4, 5.
- `chair44_blocks_indep.py` reads only stdlib, numpy and Tsiokos's `r44_solid.json` (sha256 `f320d7a0…`, as stated). It
  imports no repository code. It derives legality from pyramid geometry and `ok_pair` handles same-chair, overlap and
  contact correctly. See the end of this file for the re-run.
- `discharge_audit_indep.py`: the file → archive mapping is identical to upstream (#6).
- `nd_search` totals match the logs and README (#9). The 3D log (3 closed, 6 offset, 2178 cap of 2187, 30→44→44)
  matches the paper.
- `claim_cell` (new): every ledger claim run through it gives balanced `$…$` with balanced braces in each math chunk.
- `sci()` and the `%.0e` replacement: correct formatting.
- The cut/hinge count: `cutn = E − F + 1 = 48 − 24 + 1 = 25`, which is correct for a spanning tree of the 24-face dual
  graph.
- `|F(0)|² = 64ⁿ` in the slice figures equals N² with N = 8ⁿ, so it is correct.

## Re-run results (referenced above)

- `boundary_certificate/check_spectre_fractal.py` and `spectre_window.py`: re-run outputs are byte-identical to
  `out_spectre_fractal.txt` and `out_spectre_window.txt`.
- `python3 -I hierarchy_certificate/chair44_blocks_indep.py ../chair44_data/r44_solid.json` (13 min 17 s): output is
  identical to `out_chair44_blocks_indep.txt` except the timing lines:
  - 2388/1194/44 contacts, |P0| = 30;
  - primitive at power 3; depth-3 coincidence, 336 of 512 addresses;
  - 1410 legal blocks; 27 fixed seeds with stabilisers {1: 24, 8: 3};
  - 360,189 admissible blocks, 15,214 orbits, 0 illegal child windows.

  The numbers are right; finding #2 is only that no code asserts them.
- `python3 spectrepaper.py` and `python3 spectre_supplement.py` regenerate `spectre_substrate.tex`,
  `spectre_bigbang_note.tex` and `spectre_supplement.tex` byte-identical to the committed files, so the `.tex` files
  are generated and not hand-edited. The PDFs were not rebuilt.
